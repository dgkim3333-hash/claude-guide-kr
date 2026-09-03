# datagokr-mcp

data.go.kr 47개 공공 OpenAPI를 하나의 MCP 서버로 통합. 
선언적 메타데이터 기반으로 새 API 추가가 쉽고, 기존 `building-info` MCP의 
"no element found: line 1, column 0" XML 파싱 오류도 해결.

## 주요 설계

- **메타데이터 기반 자동 등록**: `apis/*.py`에 `ApiSpec`만 정의하면 tool 자동 생성
- **빈 응답 감지**: data.go.kr이 인증 실패 시 빈 바디를 반환해도 명확한 에러로 변환
- **표준 에러 XML 파싱**: `OpenAPI_ServiceResponse`와 `response.header.resultCode` 양쪽 구조 모두 처리
- **JSON/XML 자동 감지**: Content-Type + 바디 시그니처 둘 다 체크
- **`xmltodict` 사용**: 기존 MCP가 `xml.etree`로 터지던 케이스들을 안정적으로 파싱

## 검증 현황 (2026-04-18)

| 카테고리 | tool 수 | 상태 |
|----------|---------|------|
| 우정사업본부 도로명주소 | 1 | ✅ |
| 행안부 법정동코드 | 1 | ✅ |
| 건축HUB 건축물대장 | 9 | ✅ |
| 국토부 실거래가 | 12 | ✅ |
| 소상공인 상가정보 | 2 | ✅ |
| 캠코 온비드 | 19 | ⚠️ 1개만 확인, 나머지 활용신청 확인 필요 |
| 공동주택 단지 | 2 | ⚠️ 엔드포인트 확인 필요 |
| 도시철도 노선 | 1 | ⚠️ 엔드포인트 확인 필요 |
| **합계** | **47** | **25개 동작 확인** |

## 디렉터리 구조

```
datagokr-mcp/
├── server.py              # FastMCP 엔트리포인트
├── pyproject.toml
├── .env.example
├── CHANGELOG.md
├── scripts/
│   ├── smoke.py                    # 스모크 테스트 (12개 API)
│   └── building_bug_regression.py  # 기존 MCP 버그 재현 테스트
├── core/
│   ├── client.py          # 공통 HTTP 클라이언트 (빈 응답/에러 처리)
│   └── registry.py        # ApiSpec / Param / 레지스트리
└── apis/
    ├── epost_address.py        # 우정사업본부 도로명주소 (1) ✅
    ├── legal_dong.py           # 행안부 법정동코드 (1) ✅
    ├── building.py             # 건축HUB 건축물대장 (9) ✅
    ├── molit_realprice.py      # 국토부 실거래가 (12) ✅
    ├── onbid.py                # 캠코 온비드 (19) ⚠️
    ├── sbiz_commercial.py      # 소상공인 상가정보 (2) ✅
    └── housing_transport.py    # 공동주택 단지 + 도시철도 (3) ⚠️
```

## 설치 (로컬 PC)

### 1. 의존성 설치

```bash
cd C:\AI\mcp\datagokr-mcp
# uv 권장
uv sync
# 또는 pip
pip install -e .
```

### 2. 서비스키 설정

```bash
copy .env.example .env
# .env 편집해서 본인 키 입력
```

`DATA_GO_KR_SERVICE_KEY`는 data.go.kr 마이페이지의 **일반 인증키 (Decoding된 것)**를 사용하세요.

### 3. 등록 확인

```bash
uv run python -c "import apis; from core import all_specs; print('registered:', len(all_specs()))"
```
→ `registered: 47` 출력되면 정상.

### 4. 스모크 테스트

```bash
uv run python scripts/smoke.py
```

## Claude Desktop 연결

`%APPDATA%\Claude\claude_desktop_config.json` (Windows) 에 추가:

```json
{
  "mcpServers": {
    "datagokr": {
      "command": "uv",
      "args": [
        "--directory",
        "C:\\AI\\mcp\\datagokr-mcp",
        "run",
        "python",
        "server.py"
      ],
      "env": {
        "DATA_GO_KR_SERVICE_KEY": "본인_data.go.kr_키",
        "EPOST_SERVICE_KEY": "여기에_본인_EPOST_서비스키_입력"
      }
    }
  }
}
```

Claude Desktop 재시작 → 47개 tool이 등록됩니다.

**중요**: 기존 `building-info` MCP 항목은 주석처리 또는 삭제하세요.

## 새 API 추가 방법

1. `apis/` 아래에 파일 하나 만들기 (예: `apis/my_api.py`)
2. `register(ApiSpec(...))` 호출로 스펙 정의
3. `apis/__init__.py`에 `from . import my_api` 추가
4. 서버 재시작 → 새 tool 자동 등록

### 예시: 새 API 추가

```python
# apis/my_api.py
from core.registry import ApiSpec, Param, register, unwrap_response_body

register(ApiSpec(
    tool_name="my_new_api",
    description="새 API 설명",
    endpoint="https://apis.data.go.kr/기관코드/서비스명/오퍼레이션명",
    params=[
        Param(name="param1", py_name="my_param", type="string", required=True,
              description="파라미터 설명"),
    ],
    post_process=unwrap_response_body,
    category="custom",
))
```

## 트러블슈팅

### `EMPTY_BODY` 에러
- 서비스키가 `.env` 또는 Claude Desktop 설정에 없음
- 또는 해당 API에 활용신청이 안 되어 있음
- data.go.kr → 마이페이지 → 활용신청 현황에서 확인

### `code=30` (등록되지 않은 서비스키)
- 해당 API에 별도 활용신청 필요
- data.go.kr에서 해당 API 검색 → "활용신청" 클릭

### `code=31` (만료된 서비스키)
- data.go.kr → 마이페이지 → 인증키 관리에서 연장

### 500 "Unexpected errors"
- 엔드포인트 URL이 현행 API와 불일치
- data.go.kr > 해당 API 상세페이지 > "미리보기"에서 정확한 URL 확인
- `apis/xxx.py`의 endpoint 수정 후 서버 재시작

### 403 "Forbidden"
- 해당 엔드포인트가 폐기/변경됨 (예: RTMSDataSvcAptTradeDev → RTMSDataSvcAptTrade)
- data.go.kr 상세페이지에서 현행 URL 확인

### 서비스키 갱신
1. data.go.kr 로그인 → 마이페이지 → 인증키 관리
2. "일반 인증키" 항목의 Decoding된 키 복사
3. `.env`와 `claude_desktop_config.json` 모두 업데이트
4. Claude Desktop 재시작

### 로그 확인
- MCP 서버 로그는 stderr로 출력
- Claude Desktop의 MCP 로그 창에서 확인 가능
- 호출 실패 시 `{"error": true, "code": "...", "message": "..."}` 반환

## 기존 `building-info` MCP에서 옮겨오기

기존 tool 이름:
- `building-info:search_building` → 이 서버의 `building_basis_outline`
- `building-info:get_building_title` → 이 서버의 `building_title`

파라미터명도 같은 스타일(snake_case)이라 프롬프트 거의 그대로 작동합니다.

## 제약사항

- data.go.kr 일일 호출 한도: 개발계정 기본 1,000~10,000건 (API별 상이)
- 운영계정 전환 시 한도 확장 가능 (data.go.kr에서 신청)
- 실거래가 API는 XML 응답만 지원 (JSON 없음). `auto` 감지로 처리
- 온비드 API 서비스명이 v2(차세대)로 변경 중 — 향후 추가 수정 필요 가능
