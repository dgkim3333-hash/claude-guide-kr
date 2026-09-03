"""국토부 - 공동주택 단지정보 + 도시철도 노선 API.

NOTE (2026-04-18 검증 결과):
  - AptListService3 → 404 "API not found", AptListService → 500
  - UrbanRailroadInfoService → 500 "Unexpected errors"
  - 이 API들은 data.go.kr에서 별도 활용신청이 필요할 수 있음.
  - 활용신청 후 data.go.kr 상세페이지에서 정확한 엔드포인트 확인 필요.
"""
from core.registry import ApiSpec, Param, register, unwrap_response_body


# ---------------------------------------------------------------------------
# 공동주택 단지 목록
# ---------------------------------------------------------------------------
register(ApiSpec(
    tool_name="apt_complex_list",
    description="공동주택 단지 목록 조회. 시군구/법정동별 모든 아파트 단지 리스트.",
    endpoint="https://apis.data.go.kr/1613000/AptListService3/getLegaldongAptList",
    service_key_env="DATA_GO_KR_SERVICE_KEY",
    service_key_param="serviceKey",
    response_format="auto",
    category="housing",
    params=[
        Param(name="sigunguCode", py_name="sigungu_code", type="string", required=True,
              description="시군구코드 5자리"),
        Param(name="bjdongCode", py_name="bjdong_code", type="string", required=True,
              description="법정동코드 5자리"),
        Param(name="numOfRows", py_name="num_of_rows", type="integer", default=100),
        Param(name="pageNo", py_name="page_no", type="integer", default=1),
    ],
    post_process=unwrap_response_body,
))


register(ApiSpec(
    tool_name="apt_complex_basic_info",
    description="공동주택 단지 기본정보 조회. 단지코드(kaptCode)로 세대수, 준공일, 난방방식, 관리사무소 등 상세.",
    endpoint="https://apis.data.go.kr/1613000/AptBasisInfoServiceV3/getAphusBassInfoV3",
    service_key_env="DATA_GO_KR_SERVICE_KEY",
    service_key_param="serviceKey",
    response_format="auto",
    category="housing",
    params=[
        Param(name="kaptCode", py_name="kapt_code", type="string", required=True,
              description="공동주택관리번호 (apt_complex_list로 조회)"),
    ],
    post_process=unwrap_response_body,
))


# ---------------------------------------------------------------------------
# 도시철도 노선 (입지 분석용)
# ---------------------------------------------------------------------------
register(ApiSpec(
    tool_name="urban_rail_route",
    description="도시철도 노선 정보 조회. 역명/노선명/위도경도/운영기관 등.",
    endpoint="https://apis.data.go.kr/1613000/UrbanRailroadInfoService/getUrbanRailroadInfo",
    service_key_env="DATA_GO_KR_SERVICE_KEY",
    service_key_param="serviceKey",
    response_format="auto",
    category="transport",
    params=[
        Param(name="subwayStationName", py_name="station_name", type="string", default="",
              description="역명 (일부 매칭)"),
        Param(name="subwayRouteName", py_name="route_name", type="string", default="",
              description="노선명 (예: '2호선', '신분당선')"),
        Param(name="numOfRows", py_name="num_of_rows", type="integer", default=50),
        Param(name="pageNo", py_name="page_no", type="integer", default=1),
    ],
    post_process=unwrap_response_body,
))
