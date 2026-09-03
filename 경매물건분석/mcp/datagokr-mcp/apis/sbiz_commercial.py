"""소상공인시장진흥공단 상가(상권)정보 API

엔드포인트 베이스: https://apis.data.go.kr/B553077/api/open/sdsc2
응답: JSON

주요 엔드포인트:
  - storeZoneInOne: 반경 내 점포 조회
  - storeZoneInRect: 사각 영역 내 점포
  - storeListInRadius: 반경 내 점포 목록
  - storeListInUpjong: 업종별 점포 목록
  - storeListInDong: 법정동별 점포 목록

NPL/경매 분석 시 주변 상권 파악에 유용.
"""
from core.registry import ApiSpec, Param, register, unwrap_response_body


def _sbiz_spec(
    tool_name: str, description: str, endpoint_name: str, extra_params: list[Param],
) -> ApiSpec:
    return ApiSpec(
        tool_name=tool_name,
        description=description,
        endpoint=f"https://apis.data.go.kr/B553077/api/open/sdsc2/{endpoint_name}",
        service_key_env="DATA_GO_KR_SERVICE_KEY",
        service_key_param="ServiceKey",   # 대문자
        response_format="json",
        category="commercial",
        params=[
            *extra_params,
            Param(name="numOfRows", py_name="num_of_rows", type="integer", default=100),
            Param(name="pageNo", py_name="page_no", type="integer", default=1),
            Param(name="type", type="string", default="json"),
        ],
        post_process=unwrap_response_body,
    )


register(_sbiz_spec(
    "sbiz_stores_in_radius",
    "소상공인 상가 반경 조회. 주어진 좌표 반경 N미터 내 모든 점포 목록.",
    "storeListInRadius",
    [
        Param(name="cx", type="number", required=True, description="중심 경도(longitude)"),
        Param(name="cy", type="number", required=True, description="중심 위도(latitude)"),
        Param(name="radius", type="integer", default=500, description="반경 (미터, 최대 5000)"),
        Param(name="indsLclsCd", py_name="industry_large_code", type="string", default="",
              description="업종대분류 코드 (선택, 예: 'D'=음식업)"),
        Param(name="indsMclsCd", py_name="industry_mid_code", type="string", default="",
              description="업종중분류 코드 (선택)"),
        Param(name="indsSclsCd", py_name="industry_small_code", type="string", default="",
              description="업종소분류 코드 (선택)"),
    ],
))

register(_sbiz_spec(
    "sbiz_stores_in_dong",
    "소상공인 상가 법정동별 조회. 특정 법정동의 점포 목록.",
    "storeListInDong",
    [
        Param(name="divId", type="string", default="adongCd",
              description="구분자 고정 (adongCd=법정동코드로 조회)"),
        Param(name="key", py_name="dong_code", type="string", required=True,
              description="법정동코드 10자리"),
        Param(name="indsLclsCd", py_name="industry_large_code", type="string", default=""),
        Param(name="indsMclsCd", py_name="industry_mid_code", type="string", default=""),
        Param(name="indsSclsCd", py_name="industry_small_code", type="string", default=""),
    ],
))
