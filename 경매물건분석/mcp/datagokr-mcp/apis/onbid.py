"""한국자산관리공사(캠코) 온비드 공매 API 19종

베이스: https://apis.data.go.kr/B010003/

NOTE (2026-04-18 검증 결과):
  - B010003 기관코드가 온비드 API의 올바른 prefix.
  - 일부 API는 v2(차세대) 서비스명 사용: 예) OnbidCltrBidRsltListSrvc2
  - 대부분의 온비드 API가 data.go.kr에서 500 "Unexpected errors" 반환 →
    활용신청이 개별적으로 필요할 수 있음.
  - 확인된 동작 서비스: OnbidCltrBidRsltListSrvc2/getCltrBidRsltList2
  - 각 API의 정확한 서비스명은 data.go.kr 해당 API 상세페이지에서 확인 필요.
"""
from core.registry import ApiSpec, Param, register, unwrap_response_body

BASE_NEXT = "https://apis.data.go.kr/B010003"

_PAGE_PARAMS = [
    Param(name="numOfRows", py_name="num_of_rows", type="integer", default=20),
    Param(name="pageNo", py_name="page_no", type="integer", default=1),
    # ⚠️ v2 차세대 온비드 API는 `resultType`을 사용. `type`은 API가 무시함.
    # 이전에 `type=json`이었으나 API가 XML을 반환하는 원인이었음 (2026-04-20 수정).
    Param(name="resultType", py_name="result_type", type="string", default="json",
          description="응답형식 (json 또는 xml). v2 API는 resultType만 인식."),
]


def _onbid_spec(
    tool_name: str,
    description: str,
    service: str,          # 서비스 이름 (endpoint path 일부)
    operation: str,        # 오퍼레이션 (get...)
    extra_params: list[Param] | None = None,
) -> ApiSpec:
    return ApiSpec(
        tool_name=tool_name,
        description=description,
        endpoint=f"{BASE_NEXT}/{service}/{operation}",
        service_key_env="DATA_GO_KR_SERVICE_KEY",
        service_key_param="serviceKey",
        response_format="auto",
        category="onbid",
        params=[*(extra_params or []), *_PAGE_PARAMS],
        post_process=unwrap_response_body,
    )


# ---- 공고 조회 계열 (⚠️ 미검증 - 활용신청 필요 가능) ----
register(_onbid_spec(
    "onbid_notice_list",
    "온비드 공고목록 조회 (v2 차세대). 입찰예정/진행중/종료 공매 공고. 필수: cltrTypeCd(0001=부동산), prptDivCd(쉼표구분). 공고명 검색: onbidPbancNm. 기간: opbdDtStart/End.",
    service="OnbidPbancListSrvc2",
    operation="getPbancList2",
    extra_params=[
        Param(name="cltrTypeCd", py_name="cltr_type_cd", type="string", required=True,
              description="물건유형코드 (0001=부동산)"),
        Param(name="prptDivCd", py_name="prpt_div_cd", type="string", required=True,
              description="재산유형코드 쉼표구분. 전체: 0007,0010,0005,0004,0002,0003,0006,0008,0011,0013"),
        Param(name="opbdDtStart", py_name="opbd_dt_start", type="string",
              description="개찰시작일 (yyyyMMdd)"),
        Param(name="opbdDtEnd", py_name="opbd_dt_end", type="string",
              description="개찰종료일 (yyyyMMdd)"),
        Param(name="onbidPbancNm", py_name="onbid_pbanc_nm", type="string",
              description="공고명 검색 키워드 (예: 봉천동, 관악구)"),
        # resultType은 _PAGE_PARAMS에서 자동 포함됨
    ],
))
register(_onbid_spec(
    "onbid_notice_detail",
    "온비드 공고상세 조회. 특정 공고(PLNM_NO)의 전체 상세 정보. (v2 차세대)",
    service="OnbidPbancDtlInfSrvc2",
    operation="getPbancDtlInf2",
    extra_params=[
        Param(name="PLNM_NO", py_name="plnm_no", type="string", required=True,
              description="공고번호"),
    ],
))
register(_onbid_spec(
    "onbid_notice_bid_info",
    "온비드 공고상세 입찰정보 조회",
    service="OnbidPblancBidInfoInqireSvc",
    operation="getPblancBidInfo",
))

# ---- 물건 조회 계열 (⚠️ 미검증) ----
register(_onbid_spec(
    "onbid_realestate_list",
    "온비드 부동산 물건목록 조회 (v2 차세대). 필수: prptDivCd(쉼표구분, 전체=0007,0010,0005,0004,0002,0003,0006,0008,0011,0013). 위치: lctnSdnm, lctnSggnm. ⚠️ 구코드 0101/0201/0301 사용금지",
    service="OnbidRlstListSrvc2",
    operation="getRlstCltrList2",
    extra_params=[
        Param(name="prptDivCd", py_name="prpt_div_cd", type="string", required=True,
              description="재산유형코드 쉼표구분. 0002=공유재산,0003=금융권담보,0005=수탁재산,0007=압류재산,0008=국유재산,0010=기타일반. 전체: 0007,0010,0005,0004,0002,0003,0006,0008,0011,0013"),
        Param(name="pvctTrgtYn", py_name="pvct_trgt_yn", type="string",
              description="수의계약가능여부 (Y/N). 선택사항 — 생략 시 전체 조회"),
        Param(name="lctnSdnm", py_name="lctn_sdnm", type="string",
              description="시도 정식명 (예: 서울특별시, 경기도)"),
        Param(name="lctnSggnm", py_name="lctn_sggnm", type="string",
              description="시군구명 (예: 관악구)"),
        # resultType은 _PAGE_PARAMS에서 자동 포함됨
    ],
))
register(_onbid_spec(
    "onbid_realestate_detail",
    "온비드 부동산 물건상세 조회 (v2 차세대)",
    service="OnbidRlstDtlSrvc2",
    operation="getRlstDtlInf2",
    extra_params=[
        Param(name="CLTR_NO", py_name="cltr_no", type="string", required=True,
              description="물건번호"),
    ],
))
register(_onbid_spec(
    "onbid_movable_list",
    "온비드 동산 물건목록 조회",
    service="OnbidCltrMovableListInqireSvc",
    operation="getCltrMovableList",
))
register(_onbid_spec(
    "onbid_pblanc_thing_info",
    "온비드 공고상세 물건정보 조회",
    service="OnbidPblancThingInfoInqireSvc",
    operation="getPblancThingInfo",
))

# ---- 입찰결과 ----
# NOTE: 공고 입찰결과(Pblanc)는 차세대 API 미제공. 물건 입찰결과(Cltr) v2 사용 권장
register(_onbid_spec(
    "onbid_pblanc_bidresult_list",
    "[구버전·미사용] 온비드 공고 입찰결과목록 조회. 물건 입찰결과(onbid_cltr_bidresult_list) 사용 권장.",
    service="OnbidPblancBidRsltListInqireSvc",
    operation="getPblancBidRsltList",
))
# NOTE: 공고 입찰결과상세(Pblanc)는 차세대 API 미제공. 물건 입찰결과상세(onbid_cltr_bidresult_detail) 사용 권장
register(_onbid_spec(
    "onbid_pblanc_bidresult_detail",
    "[구버전·미사용] 온비드 공고 입찰결과상세 조회. 물건 입찰결과상세(onbid_cltr_bidresult_detail) 사용 권장.",
    service="OnbidPblancBidRsltDetlInqireSvc",
    operation="getPblancBidRsltDetl",
))
# ✅ 검증 완료 (v2 차세대 서비스명)
register(_onbid_spec(
    "onbid_cltr_bidresult_list",
    "온비드 물건 입찰결과목록 조회 (v2 차세대). 필수: cltrTypeCd(0001=부동산), prptDivCd(쉼표구분, 전체=0007,0010,0005,0004,0002,0003,0006,0008,0011,0013). 위치: lctnSdnm(시도 정식명), lctnSggnm(시군구). 기간: opbdDtStart/End(yyyyMMdd). ⚠️ 구코드 0101/0201/0301 사용금지",
    service="OnbidCltrBidRsltListSrvc2",
    operation="getCltrBidRsltList2",
    extra_params=[
        Param(name="cltrTypeCd", py_name="cltr_type_cd", type="string", required=True,
              description="물건유형코드 (0001=부동산, 0002=동산)"),
        Param(name="prptDivCd", py_name="prpt_div_cd", type="string", required=True,
              description="재산유형코드 쉼표구분. 0002=공유재산,0003=금융권담보,0004=유입자산,0005=수탁재산,0006=기타자산,0007=압류재산,0008=국유재산,0010=기타일반,0011=장기체납국세,0013=기타공자산. 전체조회: 0007,0010,0005,0004,0002,0003,0006,0008,0011,0013"),
        Param(name="opbdDtStart", py_name="opbd_dt_start", type="string", required=True,
              description="개찰시작일 (yyyyMMdd)"),
        Param(name="opbdDtEnd", py_name="opbd_dt_end", type="string", required=True,
              description="개찰종료일 (yyyyMMdd)"),
        Param(name="lctnSdnm", py_name="lctn_sdnm", type="string",
              description="시도 정식명 (예: 서울특별시, 경기도)"),
        Param(name="lctnSggnm", py_name="lctn_sggnm", type="string",
              description="시군구명 (예: 관악구, 성남시 분당구)"),
        Param(name="lctnEmdNm", py_name="lctn_emd_nm", type="string",
              description="읍면동명 (예: 봉천동)"),
        # resultType은 _PAGE_PARAMS에서 자동 포함됨
        Param(name="pvctTrgtYn", py_name="pvct_trgt_yn", type="string",
              description="수의계약가능여부 (Y/N). 선택사항"),
        Param(name="dspsMthodCd", py_name="dsps_mthod_cd", type="string",
              description="처분방식코드 (0001=매각, 0002=임대). 선택사항"),
        Param(name="bidDivCd", py_name="bid_div_cd", type="string",
              description="입찰구분코드. 선택사항"),
    ],
))
register(_onbid_spec(
    "onbid_cltr_bidresult_detail",
    "온비드 물건 입찰결과상세 조회 (v2 차세대)",
    service="OnbidCltrBidRsltDtlSrvc2",
    operation="getCltrBidRsltDtl2",
))

# ---- 순위/통계 (⚠️ 미검증) ----
register(_onbid_spec(
    "onbid_top_viewed",
    "온비드 순위물건목록 조회수 순위",
    service="OnbidTopViewedCltrInqireSvc",
    operation="getTopViewedCltr",
))
register(_onbid_spec(
    "onbid_top_favorite",
    "온비드 순위물건목록 관심물건 순위",
    service="OnbidTopFavoriteCltrInqireSvc",
    operation="getTopFavoriteCltr",
))
register(_onbid_spec(
    "onbid_top_discount",
    "온비드 순위물건목록 저감률 순위",
    service="OnbidTopDiscountCltrInqireSvc",
    operation="getTopDiscountCltr",
))
register(_onbid_spec(
    "onbid_stat_by_usage",
    "온비드 용도별 입찰 통계",
    service="OnbidBidStatByUsageInqireSvc",
    operation="getBidStatByUsage",
))
register(_onbid_spec(
    "onbid_stat_by_region",
    "온비드 지역별 입찰 통계",
    service="OnbidBidStatByRegionInqireSvc",
    operation="getBidStatByRegion",
))

# ---- 캠코 특수 물건 (⚠️ 미검증) ----
register(_onbid_spec(
    "kamco_commissioned_nonbusiness_assets",
    "캠코 수탁 비업무용 자산 매각정보",
    service="KamcoCommissionedNonbusinessAssetSvc",
    operation="getCommissionedNonbusinessAssetList",
))
register(_onbid_spec(
    "kamco_delinquent_success_rate",
    "체납 압류재산 공매 용도별/지역별 낙찰가율",
    service="KamcoDelinquentSuccessRateSvc",
    operation="getDelinquentSuccessRate",
))
register(_onbid_spec(
    "kamco_national_property_bid_list",
    "국유일반재산 입찰대상물건내역",
    service="KamcoNationalPropertyBidListSvc",
    operation="getNationalPropertyBidList",
))
