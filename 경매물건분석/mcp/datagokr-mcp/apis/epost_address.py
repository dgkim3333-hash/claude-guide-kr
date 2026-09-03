"""과학기술정보통신부 우정사업본부 - 도로명주소조회서비스

참고문서: 새주소5자리우편번호조회서비스명세서.docx
엔드포인트: https://openapi.epost.go.kr/postal/retrieveNewAdressAreaCdService
응답: XML only
인증키: 별도 발급 (.env에 EPOST_SERVICE_KEY로 저장)

상세기능: 새우편번호 도로명주소 조회
  - searchSe=road: 도로명 주소로 검색 → 도로명주소 + 지번주소 반환
  - searchSe=dong: 지번 주소(동명)로 검색 → 도로명주소 + 지번주소 반환
"""
from core.registry import ApiSpec, Param, register, unwrap_response_body


def _post_epost(data: dict) -> dict:
    """우편번호 API는 고유 응답 스키마.

    <NewAddressListResponse>
      <cmmMsgHeader>...</cmmMsgHeader>
      <newAddressListAreaCd>
        <zipNo>...</zipNo>
        <lnmAdres>지번주소</lnmAdres>
        <rnAdres>도로명주소</rnAdres>
        ...
      </newAddressListAreaCd>
      ...
    </NewAddressListResponse>
    """
    root = data.get("NewAddressListResponse") or data
    if not isinstance(root, dict):
        return {"items": [], "raw": data}

    items_node = root.get("newAddressListAreaCd")
    if items_node is None:
        items: list = []
    elif isinstance(items_node, list):
        items = items_node
    else:
        items = [items_node]

    header = root.get("cmmMsgHeader") or {}
    return {
        "items": items,
        "total_count": _safe_int(header.get("totalCount")),
        "count_per_page": _safe_int(header.get("countPerPage")),
        "current_page": _safe_int(header.get("currentPage")),
    }


def _safe_int(v):
    try:
        return int(v) if v not in (None, "") else None
    except (TypeError, ValueError):
        return None


register(ApiSpec(
    tool_name="epost_address_search",
    description=(
        "우정사업본부 도로명주소조회. 도로명 주소 또는 지번 주소로 검색해서 "
        "일치하는 도로명주소 + 지번주소 + 5자리 우편번호를 모두 반환한다. "
        "searchSe='road'면 도로명으로 검색, 'dong'이면 지번(동명)으로 검색."
    ),
    endpoint="http://openapi.epost.go.kr/postal/retrieveNewAdressAreaCdService/retrieveNewAdressAreaCdService/getNewAddressListAreaCd",
    service_key_env="EPOST_SERVICE_KEY",
    service_key_param="serviceKey",
    response_format="auto",
    category="address",
    params=[
        Param(
            name="searchSe",
            py_name="search_type",
            type="string",
            required=True,
            enum=["road", "dong"],
            description="검색구분. 'road'=도로명주소 검색, 'dong'=지번/동명 검색",
        ),
        Param(
            name="srchwrd",
            py_name="keyword",
            type="string",
            required=True,
            description="검색어 (예: '테헤란로 152', '서현동 263')",
        ),
        Param(
            name="countPerPage",
            py_name="count_per_page",
            type="integer",
            default=10,
            description="페이지당 결과 수 (기본 10, 최대 100)",
        ),
        Param(
            name="currentPage",
            py_name="page",
            type="integer",
            default=1,
            description="페이지 번호 (1부터)",
        ),
    ],
    post_process=_post_epost,
))
