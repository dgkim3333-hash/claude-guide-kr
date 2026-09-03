"""
API 메타데이터 스키마 및 레지스트리.

각 data.go.kr API는 `ApiSpec` dataclass로 선언한다.
server.py가 모든 ApiSpec을 읽어 FastMCP tool로 자동 등록한다.

새 API 추가 = apis/ 아래 파일 하나 만들어서 SPEC 리스트에 append.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Literal


ParamType = Literal["string", "integer", "number", "boolean"]


@dataclass
class Param:
    """API 쿼리 파라미터 스펙."""

    name: str                              # data.go.kr 쪽 실제 파라미터명 (예: "LAWD_CD")
    type: ParamType = "string"
    required: bool = False
    default: Any = None
    description: str = ""
    # tool 인자명으로 쓸 snake_case 이름. 생략 시 name을 그대로 사용.
    py_name: str | None = None
    # enum 값 제한 (있으면 LLM이 선택지로 인식)
    enum: list[str] | None = None

    @property
    def tool_arg(self) -> str:
        return self.py_name or self.name


@dataclass
class ApiSpec:
    """단일 data.go.kr API의 선언적 정의."""

    # MCP tool 이름. Claude에 노출되는 식별자.
    tool_name: str
    # 사람이 읽는 한글/영문 설명. tool description에 그대로 들어감.
    description: str
    # 전체 엔드포인트 URL
    endpoint: str
    # 파라미터 목록
    params: list[Param] = field(default_factory=list)

    # 서비스키가 들어 있는 환경변수 이름
    service_key_env: str = "DATA_GO_KR_SERVICE_KEY"
    # 서비스키 파라미터명 (API마다 다름: serviceKey / ServiceKey / confmKey / authKey)
    service_key_param: str = "serviceKey"
    # 응답 포맷 강제. "auto"면 Content-Type + 바디 시그니처로 판단.
    response_format: Literal["auto", "json", "xml"] = "auto"

    # 응답 후처리 함수. (dict) -> dict. 노이즈 제거, items 평탄화 등.
    post_process: Callable[[dict[str, Any]], dict[str, Any]] | None = None

    # 카테고리 태그 (README/도움말용)
    category: str = "misc"


# ---------------------------------------------------------------------------
# 전역 레지스트리
# ---------------------------------------------------------------------------
_REGISTRY: list[ApiSpec] = []


def register(spec: ApiSpec) -> ApiSpec:
    """ApiSpec을 전역 레지스트리에 추가."""
    if any(s.tool_name == spec.tool_name for s in _REGISTRY):
        raise ValueError(f"중복된 tool_name: {spec.tool_name}")
    _REGISTRY.append(spec)
    return spec


def all_specs() -> list[ApiSpec]:
    return list(_REGISTRY)


# ---------------------------------------------------------------------------
# 공통 응답 후처리 유틸
# ---------------------------------------------------------------------------
def unwrap_response_body(data: dict[str, Any]) -> dict[str, Any]:
    """`response.body` 구조를 벗겨내서 items만 돌려준다.

    data.go.kr 대부분의 API는 다음과 같은 형태:
        {
          "response": {
            "header": {"resultCode": "00", "resultMsg": "NORMAL"},
            "body": {
              "items": {"item": [...] | {...}},
              "numOfRows": "10",
              "pageNo": "1",
              "totalCount": "123"
            }
          }
        }

    이 함수는 items만 뽑아 평탄화하고 pagination 정보를 top-level에 둠.
    """
    resp = data.get("response") or data
    body = resp.get("body") if isinstance(resp, dict) else None
    if not isinstance(body, dict):
        return data

    items_node = body.get("items")
    items: list[Any]
    if items_node is None or items_node == "":
        items = []
    elif isinstance(items_node, dict):
        inner = items_node.get("item")
        if inner is None:
            items = []
        elif isinstance(inner, list):
            items = inner
        else:
            items = [inner]
    elif isinstance(items_node, list):
        items = items_node
    else:
        items = []

    return {
        "items": items,
        "total_count": _safe_int(body.get("totalCount")),
        "page_no": _safe_int(body.get("pageNo")),
        "num_of_rows": _safe_int(body.get("numOfRows")),
    }


def _safe_int(v: Any) -> int | None:
    if v is None or v == "":
        return None
    try:
        return int(v)
    except (TypeError, ValueError):
        return None
