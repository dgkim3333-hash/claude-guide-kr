"""국토교통부 건축HUB 건축물대장정보 서비스

엔드포인트 베이스: https://apis.data.go.kr/1613000/BldRgstHubService
응답: JSON (_type=json 파라미터 필수)

세부 기능:
  - 기본개요 (getBrBasisOulnInfo)
  - 총괄표제부 (getBrRecapTitleInfo)
  - 표제부 (getBrTitleInfo)
  - 층별개요 (getBrFlrOulnInfo)
  - 부속지번 (getBrAtchJibunInfo)
  - 전유공용면적 (getBrExposPubuseAreaInfo)
  - 오수정화시설 (getBrWclfInfo)
  - 주택가격 (getBrHsprcInfo)
  - 전유부 (getBrExposInfo)

기존 building-info MCP의 XML 파싱 오류 원인:
  - (추정) 서비스키가 등록 안 됨 → 인증실패 응답 → 빈 바디 → ET.fromstring("") 터짐
  - 해결: .env에 DATA_GO_KR_SERVICE_KEY 등록 + client.py의 빈 응답 감지
"""
from core.registry import ApiSpec, Param, register, unwrap_response_body

BASE = "https://apis.data.go.kr/1613000/BldRgstHubService"

# 모든 건축물대장 API가 공유하는 파라미터
_COMMON_PARAMS = [
    Param(
        name="sigunguCd",
        py_name="sigungu_cd",
        type="string",
        required=True,
        description="시군구코드 5자리 (예: 서울 강남구='11680')",
    ),
    Param(
        name="bjdongCd",
        py_name="bjdong_cd",
        type="string",
        required=True,
        description="법정동코드 5자리 (예: 역삼동='10100')",
    ),
    Param(
        name="platGbCd",
        py_name="plat_gb_cd",
        type="string",
        default="0",
        enum=["0", "1", "2"],
        description="대지구분코드. 0=대지, 1=산, 2=블록",
    ),
    Param(
        name="bun",
        py_name="bun",
        type="string",
        default="",
        description="번지 4자리 (예: '0737'). 생략 가능.",
    ),
    Param(
        name="ji",
        py_name="ji",
        type="string",
        default="",
        description="지 4자리 (예: '0000'). 생략 가능.",
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
        description="페이지 번호",
    ),
    Param(
        name="_type",
        type="string",
        default="json",
        description="응답 포맷 (고정값 json)",
    ),
]


def _endpoint_spec(suffix: str, tool_name: str, description: str) -> ApiSpec:
    return ApiSpec(
        tool_name=tool_name,
        description=description,
        endpoint=f"{BASE}/{suffix}",
        service_key_env="DATA_GO_KR_SERVICE_KEY",
        service_key_param="serviceKey",
        response_format="json",
        category="building",
        params=list(_COMMON_PARAMS),
        post_process=unwrap_response_body,
    )


register(_endpoint_spec(
    "getBrBasisOulnInfo",
    "building_basis_outline",
    "건축물대장 기본개요. 위치, 대지면적, 연면적, 건물용도, 구조, 허가일 등 기본 요약 정보.",
))
register(_endpoint_spec(
    "getBrRecapTitleInfo",
    "building_recap_title",
    "건축물대장 총괄표제부. 하나의 대지에 여러 동이 있을 때 총괄 정보 (단일동 건물에는 없음).",
))
register(_endpoint_spec(
    "getBrTitleInfo",
    "building_title",
    "건축물대장 표제부. 동별 대표 정보 - 연면적, 용적률, 건폐율, 구조, 주용도, 층수, 승강기 등.",
))
register(_endpoint_spec(
    "getBrFlrOulnInfo",
    "building_floor_outline",
    "건축물대장 층별개요. 각 층의 용도와 면적.",
))
register(_endpoint_spec(
    "getBrAtchJibunInfo",
    "building_attached_jibun",
    "건축물대장 부속지번. 주된 지번 외 부속된 지번 목록.",
))
register(_endpoint_spec(
    "getBrExposPubuseAreaInfo",
    "building_expos_pubuse_area",
    "건축물대장 전유공용면적. 구분소유 건물의 호별 전유면적/공용면적.",
))
register(_endpoint_spec(
    "getBrWclfInfo",
    "building_wastewater",
    "건축물대장 오수정화시설 정보.",
))
register(_endpoint_spec(
    "getBrHsprcInfo",
    "building_housing_price",
    "건축물대장 주택가격. 공시가격 이력.",
))
register(_endpoint_spec(
    "getBrExposInfo",
    "building_expos",
    "건축물대장 전유부. 호별 상세 (호명, 전유면적, 용도 등).",
))
