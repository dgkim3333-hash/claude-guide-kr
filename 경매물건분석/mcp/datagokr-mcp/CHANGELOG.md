# CHANGELOG — datagokr-mcp

## v0.1.0 (2026-04-18) — 초기 구축 및 검증

### 엔드포인트 수정

| API | 수정 전 | 수정 후 | 사유 |
|-----|---------|---------|------|
| `epost_address_search` | `https://openapi.epost.go.kr/postal/retrieveNewAdressAreaCdService` | `http://openapi.epost.go.kr/postal/retrieveNewAdressAreaCdService/retrieveNewAdressAreaCdService/getNewAddressListAreaCd` | 서비스명 반복 + 오퍼레이션명 누락. 프로토콜 http |
| `epost_address_search` | `response_format="xml"` | `response_format="auto"` | 실제 응답이 JSON으로 반환됨 |
| `realprice_apt_trade` | `RTMSDataSvcAptTradeDev/getRTMSDataSvcAptTradeDev` | `RTMSDataSvcAptTrade/getRTMSDataSvcAptTrade` | Dev 버전 403 Forbidden. non-Dev가 정상 동작 |
| 온비드 전체 | `BASE_NEXT = .../1360000` | `BASE_NEXT = .../B010003` | 기관코드 1360000은 기상청. 캠코=B010003 |
| `onbid_cltr_bidresult_list` | `OnbidCltrBidRsltListInqireSvc/getCltrBidRsltList` | `OnbidCltrBidRsltListSrvc2/getCltrBidRsltList2` | v2(차세대) 서비스명으로 확인 |

### 버그 수정

| 항목 | 내용 |
|------|------|
| `core/client.py` 에러 코드 판정 | `resultCode="000"` (실거래가 API 정상 응답)을 에러로 판정하던 문제 수정. `("00", "0", "000")` 모두 성공으로 인식 |
| 기존 `building-info` MCP XML 크래시 | `xml.etree.ElementTree.ParseError: no element found` 버그 해결 — 빈 응답 감지 + xmltodict 사용 + 명시적 에러 메시지 |

### 검증 결과 (2026-04-18)

**✅ 동작 확인 (25개)**

| 카테고리 | tool 수 | 상태 |
|----------|---------|------|
| address — epost | 1 | ✅ 완전 동작 |
| address — legal_dong | 1 | ✅ 완전 동작 |
| building (건축물대장 9종) | 9 | ✅ 완전 동작 |
| realprice (실거래가 12종) | 12 | ✅ 완전 동작 |
| commercial (상가정보 2종) | 2 | ✅ 완전 동작 |

**⚠️ 미확인 / 활용신청 필요 (22개)**

| 카테고리 | tool 수 | 증상 | 조치 |
|----------|---------|------|------|
| onbid (19종 중 18종) | 18 | 500 "Unexpected errors" | data.go.kr에서 해당 API별 활용신청 필요. 서비스명이 v2로 변경되었을 수 있음 |
| onbid_cltr_bidresult_list | 1 | ✅ v2 확인됨 | `Srvc2` 패턴 적용 완료 |
| housing (공동주택 2종) | 2 | 404/500 | 엔드포인트 확인 필요 (AptListService3 → 미존재) |
| transport (도시철도 1종) | 1 | 500 | 엔드포인트 확인 필요 |

### 향후 조치

1. **온비드 18개 API**: data.go.kr > 마이페이지 > 활용신청 현황에서 온비드 관련 API 구독 확인. 각 API 상세페이지의 "미리보기"에서 정확한 서비스명/오퍼레이션명 확인 후 `apis/onbid.py` 업데이트
2. **공동주택 단지 API**: `AptListService` 시리즈의 현행 엔드포인트 확인 (v2/v3 모두 미동작)
3. **도시철도 노선 API**: `UrbanRailroadInfoService` 현행 여부 확인
