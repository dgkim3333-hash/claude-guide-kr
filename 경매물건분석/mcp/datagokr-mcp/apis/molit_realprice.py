"""국토교통부 실거래가 공개 서비스

엔드포인트 베이스: https://apis.data.go.kr/1613000/
각 주택유형/거래유형별로 별도 서비스 URL 존재.

공통 파라미터:
  - LAWD_CD: 시군구코드 5자리 (법정동 10자리 중 앞 5자리)
  - DEAL_YMD: 계약년월 YYYYMM (예: '202601')

응답: XML 전용 (일부 API는 JSON 지원. 여기선 안전하게 auto 감지)
"""
from core.registry import ApiSpec, Param, register, unwrap_response_body

# ---------------------------------------------------------------------------
# 공통 파라미터
# ---------------------------------------------------------------------------
_BASE_PARAMS = [
    Param(
        name="LAWD_CD",
        py_name="lawd_cd",
        type="string",
        required=True,
        description="시군구코드 5자리 (법정동코드 앞 5자리, 예: 강남구='11680')",
    ),
    Param(
        name="DEAL_YMD",
        py_name="deal_ym",
        type="string",
        required=True,
        description="계약년월 YYYYMM (예: '202601')",
    ),
    Param(
        name="numOfRows",
        py_name="num_of_rows",
        type="integer",
        default=100,
    ),
    Param(
        name="pageNo",
        py_name="page_no",
        type="integer",
        default=1,
    ),
]


def _realprice_spec(
    tool_name: str, description: str, service_path: str, endpoint_name: str,
) -> ApiSpec:
    return ApiSpec(
        tool_name=tool_name,
        description=description,
        endpoint=f"https://apis.data.go.kr/1613000/{service_path}/{endpoint_name}",
        service_key_env="DATA_GO_KR_SERVICE_KEY",
        service_key_param="serviceKey",
        response_format="auto",
        category="realprice",
        params=list(_BASE_PARAMS),
        post_process=unwrap_response_body,
    )


# ---------------------------------------------------------------------------
# 매매 실거래가
# ---------------------------------------------------------------------------
register(_realprice_spec(
    "realprice_apt_trade",
    "아파트 매매 실거래가 (국토부 공식 자료)",
    "RTMSDataSvcAptTrade",
    "getRTMSDataSvcAptTrade",
))
register(_realprice_spec(
    "realprice_officetel_trade",
    "오피스텔 매매 실거래가",
    "RTMSDataSvcOffiTrade",
    "getRTMSDataSvcOffiTrade",
))
register(_realprice_spec(
    "realprice_rowhouse_trade",
    "연립다세대 매매 실거래가",
    "RTMSDataSvcRHTrade",
    "getRTMSDataSvcRHTrade",
))
register(_realprice_spec(
    "realprice_sh_trade",
    "단독/다가구 매매 실거래가",
    "RTMSDataSvcSHTrade",
    "getRTMSDataSvcSHTrade",
))
register(_realprice_spec(
    "realprice_land_trade",
    "토지 매매 실거래가",
    "RTMSDataSvcLandTrade",
    "getRTMSDataSvcLandTrade",
))
register(_realprice_spec(
    "realprice_industrial_trade",
    "공장/창고 등 부동산 매매 실거래가",
    "RTMSDataSvcInduTrade",
    "getRTMSDataSvcInduTrade",
))
register(_realprice_spec(
    "realprice_commercial_trade",
    "상업업무용 부동산 매매 실거래가 (상가, 사무실 등)",
    "RTMSDataSvcNrgTrade",
    "getRTMSDataSvcNrgTrade",
))
register(_realprice_spec(
    "realprice_apt_silvertaek",
    "아파트 분양권전매 실거래가",
    "RTMSDataSvcSilvTrade",
    "getRTMSDataSvcSilvTrade",
))

# ---------------------------------------------------------------------------
# 전월세 실거래가
# ---------------------------------------------------------------------------
register(_realprice_spec(
    "realprice_apt_rent",
    "아파트 전월세 실거래가",
    "RTMSDataSvcAptRent",
    "getRTMSDataSvcAptRent",
))
register(_realprice_spec(
    "realprice_officetel_rent",
    "오피스텔 전월세 실거래가",
    "RTMSDataSvcOffiRent",
    "getRTMSDataSvcOffiRent",
))
register(_realprice_spec(
    "realprice_rowhouse_rent",
    "연립다세대 전월세 실거래가",
    "RTMSDataSvcRHRent",
    "getRTMSDataSvcRHRent",
))
register(_realprice_spec(
    "realprice_sh_rent",
    "단독/다가구 전월세 실거래가",
    "RTMSDataSvcSHRent",
    "getRTMSDataSvcSHRent",
))
