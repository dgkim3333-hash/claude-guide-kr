"""
data.go.kr 공통 HTTP 클라이언트

기존 building-info MCP의 "no element found: line 1, column 0" 버그는
data.go.kr이 인증 실패 시 빈 바디 또는 비표준 XML을 반환할 때
그대로 ET.fromstring()에 넘겨서 터지는 문제였음.

이 클라이언트는:
  1. 빈 응답을 명시적으로 감지해서 DataGoKrError 발생
  2. data.go.kr 에러 XML (OpenAPI_ServiceResponse)도 파싱해서 의미있는 메시지 반환
  3. JSON/XML 응답 자동 감지 (Content-Type + 바디 시그니처 둘 다 체크)
  4. 서비스키 URL 인코딩 이슈(+, = 등)를 자동 처리
"""
from __future__ import annotations

import os
import json
import logging
from typing import Any
from urllib.parse import urlparse, parse_qs, urlencode

import httpx
import xmltodict

log = logging.getLogger(__name__)


class DataGoKrError(Exception):
    """data.go.kr API 호출 실패 시 발생하는 예외."""

    def __init__(self, message: str, *, code: str | None = None, raw: str | None = None):
        super().__init__(message)
        self.code = code
        self.raw = raw

    def __str__(self) -> str:
        if self.code:
            return f"[{self.code}] {self.args[0]}"
        return str(self.args[0])


# data.go.kr 표준 에러 코드 매핑 (OpenAPI_ServiceResponse)
_SERVICE_ERROR_CODES = {
    "00": "정상",
    "01": "어플리케이션 에러",
    "02": "DB 에러",
    "03": "데이터 없음",
    "04": "HTTP 에러",
    "05": "서비스 연결 실패",
    "10": "잘못된 요청 파라미터",
    "11": "필수 요청 파라미터 누락",
    "12": "해당 오픈API 서비스가 없거나 폐기됨",
    "20": "서비스 접근거부",
    "21": "일시적으로 사용할 수 없는 서비스 키",
    "22": "서비스 요청제한횟수 초과",
    "30": "등록되지 않은 서비스키",
    "31": "기한 만료된 서비스키",
    "32": "등록되지 않은 IP",
    "33": "서명되지 않은 호출",
    "99": "기타 에러",
}


class DataGoKrClient:
    """data.go.kr / 공공 OpenAPI 공통 HTTP 클라이언트."""

    def __init__(
        self,
        default_service_key_env: str = "DATA_GO_KR_SERVICE_KEY",
        timeout: float = 15.0,
    ):
        self._default_key_env = default_service_key_env
        self._client = httpx.AsyncClient(
            timeout=timeout,
            headers={"Accept": "application/json, text/xml, */*"},
            follow_redirects=True,
        )

    async def aclose(self) -> None:
        await self._client.aclose()

    # ---------------------------------------------------------------------
    # Public API
    # ---------------------------------------------------------------------
    async def get(
        self,
        endpoint: str,
        params: dict[str, Any],
        *,
        service_key_env: str | None = None,
        service_key_param: str = "serviceKey",
        response_format: str = "auto",  # "auto" | "json" | "xml"
    ) -> dict[str, Any]:
        """data.go.kr API GET 호출 후 dict로 반환.

        Args:
            endpoint: 전체 URL (https://...)
            params: 쿼리 파라미터 (serviceKey 제외)
            service_key_env: 서비스키 환경변수 이름. None이면 default 사용.
            service_key_param: 서비스키 파라미터명. API마다 `serviceKey` / `ServiceKey` /
                              `confmKey` / `authKey` 등 다름.
            response_format: 응답 포맷. "auto"는 Content-Type/바디로 자동 판정.

        Returns:
            파싱된 응답 dict.

        Raises:
            DataGoKrError: 빈 응답, 인증 실패, API 에러 응답 등.
        """
        service_key = self._load_service_key(service_key_env)

        # `_type=json`을 지원하는 API는 params에 포함되어 있을 것.
        # 서비스키는 인코딩/디코딩 충돌 회피를 위해 raw URL에 직접 삽입.
        query = {service_key_param: service_key, **params}

        try:
            resp = await self._client.get(endpoint, params=query)
        except httpx.HTTPError as e:
            raise DataGoKrError(f"네트워크 오류: {e}") from e

        body = resp.text or ""
        if not body.strip():
            # 기존 MCP가 터졌던 바로 그 지점.
            raise DataGoKrError(
                f"빈 응답 (status={resp.status_code}). "
                f"서비스키 미등록/만료 혹은 엔드포인트 HTTPS 스킴 불일치 가능성이 높음.",
                code="EMPTY_BODY",
                raw=body,
            )

        # data.go.kr 서버 에러 (평문 텍스트) 조기 감지
        stripped = body.strip()
        _KNOWN_SERVER_ERRORS = {
            "Unexpected errors": "data.go.kr 서버 내부 오류. 엔드포인트 URL이 잘못되었거나 해당 API가 비활성 상태일 수 있음.",
            "API not found": "data.go.kr에 해당 API 경로가 존재하지 않음. 엔드포인트 URL 확인 필요.",
            "Forbidden": "접근 거부됨. 해당 API 활용신청 미완료 또는 엔드포인트 폐기/변경 가능성.",
        }
        for pattern, message in _KNOWN_SERVER_ERRORS.items():
            if stripped == pattern or stripped.startswith(pattern):
                raise DataGoKrError(
                    f"{message} (응답: {stripped[:100]})",
                    code="SERVER_ERROR",
                    raw=body,
                )

        # 포맷 판별
        fmt = response_format
        if fmt == "auto":
            fmt = self._detect_format(resp.headers.get("content-type", ""), body)

        if fmt == "json":
            data = self._parse_json(body)
        else:
            data = self._parse_xml(body)

        # data.go.kr 표준 에러 XML 래핑 구조 감지
        self._raise_if_error(data, raw=body)
        return data

    # ---------------------------------------------------------------------
    # Internals
    # ---------------------------------------------------------------------
    def _load_service_key(self, env: str | None) -> str:
        key_env = env or self._default_key_env
        key = os.environ.get(key_env)
        if not key:
            raise DataGoKrError(
                f"환경변수 {key_env}가 설정되지 않음. "
                f".env 또는 MCP 서버 실행 환경에 서비스키를 등록하세요.",
                code="NO_SERVICE_KEY",
            )
        return key

    @staticmethod
    def _detect_format(content_type: str, body: str) -> str:
        ct = content_type.lower()
        if "json" in ct:
            return "json"
        if "xml" in ct or "html" in ct:
            return "xml"
        # Content-Type이 틀린 경우가 많아 바디 첫 문자로도 판정
        stripped = body.lstrip()
        if stripped.startswith("{") or stripped.startswith("["):
            return "json"
        return "xml"

    @staticmethod
    def _parse_json(body: str) -> dict[str, Any]:
        try:
            return json.loads(body)
        except json.JSONDecodeError as e:
            raise DataGoKrError(
                f"JSON 파싱 실패: {e}. 응답 앞 200자: {body[:200]!r}",
                code="PARSE_JSON_FAIL",
                raw=body,
            ) from e

    @staticmethod
    def _parse_xml(body: str) -> dict[str, Any]:
        try:
            return xmltodict.parse(body)
        except Exception as e:  # xml.parsers.expat.ExpatError 등
            raise DataGoKrError(
                f"XML 파싱 실패: {e}. 응답 앞 200자: {body[:200]!r}",
                code="PARSE_XML_FAIL",
                raw=body,
            ) from e

    @staticmethod
    def _raise_if_error(data: dict[str, Any], *, raw: str) -> None:
        """data.go.kr 표준 에러 응답 구조를 감지해서 예외로 변환."""
        # 패턴 1: <OpenAPI_ServiceResponse><cmmMsgHeader>...<returnReasonCode>30</returnReasonCode>...
        svc_resp = data.get("OpenAPI_ServiceResponse") if isinstance(data, dict) else None
        if isinstance(svc_resp, dict):
            header = svc_resp.get("cmmMsgHeader") or {}
            code = header.get("returnReasonCode")
            msg = header.get("errMsg") or header.get("returnAuthMsg") or ""
            if code and code != "00":
                meaning = _SERVICE_ERROR_CODES.get(code, "알 수 없는 에러")
                raise DataGoKrError(
                    f"{meaning} ({msg})".strip(),
                    code=code,
                    raw=raw,
                )

        # 패턴 2: <response><header><resultCode>30</resultCode>...
        response = data.get("response") if isinstance(data, dict) else None
        if isinstance(response, dict):
            header = response.get("header") or {}
            code = header.get("resultCode")
            msg = header.get("resultMsg") or ""
            if code and str(code) not in ("00", "0", "000"):
                raise DataGoKrError(
                    f"{msg}".strip() or f"result_code={code}",
                    code=str(code),
                    raw=raw,
                )
