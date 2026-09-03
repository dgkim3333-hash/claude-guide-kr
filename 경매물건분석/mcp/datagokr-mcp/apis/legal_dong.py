"""행정안전부 행정표준코드 - 법정동코드 조회

엔드포인트: https://apis.data.go.kr/1741000/StanReginCd/getStanReginCdList
응답: JSON

건축물대장, 실거래가 등 거의 모든 부동산 API가 시군구코드/법정동코드를 요구.
이 API가 그 코드를 조회하는 기초 도구.
"""
from core.registry import ApiSpec, Param, register, unwrap_response_body


def _post_regioncode(data: dict) -> dict:
    """행안부 표준코드 API는 응답 스키마가 조금 다름.

    {
      "StanReginCd": [
        {"head": [{"totalCount": ..., "numOfRows": ...}, {"resultCode": "INFO-000"}]},
        {"row": [{"region_cd": ..., "locatadd_nm": ...}, ...]}
      ]
    }
    """
    node = data.get("StanReginCd")
    if not isinstance(node, list) or len(node) < 2:
        return {"items": [], "raw": data}

    head = node[0].get("head", []) if isinstance(node[0], dict) else []
    rows_node = node[1]
    rows = rows_node.get("row", []) if isinstance(rows_node, dict) else []
    if not isinstance(rows, list):
        rows = [rows]

    # head에서 totalCount 추출
    total = None
    for h in head:
        if isinstance(h, dict) and "totalCount" in h:
            try:
                total = int(h["totalCount"])
            except (TypeError, ValueError):
                total = None
            break

    return {"items": rows, "total_count": total}


register(ApiSpec(
    tool_name="legal_dong_code_search",
    description=(
        "행정안전부 법정동코드 조회. 주소 키워드(예: '강남구 역삼동')로 "
        "10자리 법정동코드(region_cd)와 전체 주소명(locatadd_nm)을 검색한다. "
        "건축물대장, 실거래가 등 다른 API가 요구하는 시군구코드(앞5자리)/법정동코드(뒤5자리) 원천."
    ),
    endpoint="https://apis.data.go.kr/1741000/StanReginCd/getStanReginCdList",
    service_key_env="DATA_GO_KR_SERVICE_KEY",
    service_key_param="ServiceKey",   # ← 이 API는 대문자 S!
    response_format="json",
    category="address",
    params=[
        Param(
            name="locatadd_nm",
            py_name="keyword",
            type="string",
            required=True,
            description="주소 검색어 (예: '강남구 역삼동', '성남시 분당구')",
        ),
        Param(
            name="numOfRows",
            py_name="num_of_rows",
            type="integer",
            default=10,
            description="페이지당 결과 수",
        ),
        Param(
            name="pageNo",
            py_name="page_no",
            type="integer",
            default=1,
        ),
        Param(
            name="type",
            type="string",
            default="json",
            description="응답 포맷 (고정 json)",
        ),
    ],
    post_process=_post_regioncode,
))
