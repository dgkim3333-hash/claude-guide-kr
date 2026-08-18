# 필요한 MCP — 네 개만 붙입니다

MCP(Model Context Protocol)는 Claude가 바깥 자료를 직접 가져오게 해주는 연결 장치입니다.

**하나도 안 붙여도 서류만으로 분석은 됩니다.** 다만 시세·법령을 못 가져와서
`[확인 필요]` 가 많아집니다. 아래 순서대로 하나씩 늘리세요.

---

## 미리 만들 폴더

소스를 받아 두는 곳입니다. **`C:\AI` 폴더 안에 `mcp` 폴더를** 만드십시오.

```
C:\AI\mcp\
```

수강생 전원이 같은 경로를 써야 **설정 파일을 그대로 복사해 쓸 수 있습니다.**
다른 곳에 두면 경로를 일일이 고쳐야 합니다.

---

## 1순위 — `korean-law` (국가법령정보센터)

| | |
|---|---|
| 안 붙이면 | 세율·법령을 **기억에 의존**합니다. 세법은 자주 바뀌어서 위험합니다 |
| 붙이면 | 조문을 그 자리에서 읽고 **법령명·시행일까지 근거로 남깁니다** |
| 설치 | **폴더가 필요 없습니다.** 설정에 한 줄이면 끝 |

공개 패키지입니다 — https://github.com/chrisryugj/korean-law-mcp

```json
"korean-law": {
  "command": "npx",
  "args": ["-y", "korean-law-mcp"],
  "env": { "LAW_OC": "발급받은_OC" }
}
```

**OC 발급** — https://open.law.go.kr 에서 신청합니다. 무료이고 **이메일 아이디**가 곧 OC입니다.

---

## 2순위 — `real-estate` (국토교통부 실거래가)

| | |
|---|---|
| 안 붙이면 | **시세 대조를 못 합니다.** 감정가가 적정한지 판단할 근거가 사라집니다 |
| 붙이면 | 아파트·단독·빌라·오피스텔의 **매매·전월세 실거래가** |

공개 저장소입니다 — https://github.com/tae0y/real-estate-mcp

**받는 법** — 위 주소에서 초록색 `Code` 버튼 → `Download ZIP` → 압축을 풀어
`C:\AI\mcp\real-estate-mcp\` 으로 이름을 맞춥니다.

```json
"real-estate": {
  "command": "uv",
  "args": ["run", "--directory", "C:\\AI\\mcp\\real-estate-mcp", "python", "src/real_estate/mcp_server/server.py"],
  "env": { "PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1" }
}
```

키는 공공데이터포털에서 받습니다. **필요한 키 이름과 신청할 서비스는 저장소 README를 따릅니다.**

---

## 3순위 — `datagokr` (공공데이터포털 묶음)

| | |
|---|---|
| 붙이면 | **건축물대장** · 반경 500m **상권** · **온비드 공매** · 실거래가 보조 |
| 주의 | **설치가 가장 까다롭습니다.** 수업 시간에 같이 합니다 |

설치 순서는 교재와 `claude_desktop_config_실습용.jsonc` 를 따릅니다.
소스는 `C:\AI\mcp\datagokr-mcp\` 에 둡니다.

```json
"datagokr": {
  "command": "uv",
  "args": ["--directory", "C:\\AI\\mcp\\datagokr-mcp", "run", "python", "server.py"],
  "env": {
    "DATA_GO_KR_SERVICE_KEY": "공공데이터포털_인증키",
    "PYTHONIOENCODING": "utf-8",
    "PYTHONUTF8": "1"
  }
}
```

---

## 4순위 — `vworld-landuse` (브이월드 공간정보)

| | |
|---|---|
| 붙이면 | **개별공시지가** · 용도지역 · 토지이용계획을 주소만으로 |

이 저장소에 들어 있습니다 — [경매물건분석/mcp/vworld-landuse-mcp](mcp/vworld-landuse-mcp)
그 폴더를 `C:\AI\mcp\vworld-landuse-mcp\` 로 복사하고, 안에 들어 있는 README를 따릅니다.

```json
"vworld-landuse": {
  "command": "uv",
  "args": ["run", "--directory", "C:\\AI\\mcp\\vworld-landuse-mcp", "python", "vworld_landuse_mcp.py"],
  "env": {
    "VWORLD_API_KEY": "발급받은_브이월드_키",
    "PYTHONIOENCODING": "utf-8",
    "PYTHONUTF8": "1"
  }
}
```

**브이월드 키는 각자 받아야 합니다.** 남의 키를 같이 쓰면 호출 한도를 같이 소진합니다.
**개발키는 6개월짜리**니 만료 전에 연장하십시오.

---

## 인증키 발급처

| 발급처 | 주소 | 쓰는 곳 |
|---|---|---|
| 공공데이터포털 | https://www.data.go.kr | `real-estate` · `datagokr` |
| 국가법령정보센터 | https://open.law.go.kr | `korean-law` (OC) |
| 브이월드 | https://www.vworld.kr | `vworld-landuse` |

**공공데이터포털은 키 하나로 여러 서비스를 씁니다.** 다만 서비스마다
**활용신청**을 따로 눌러야 그 서비스가 열립니다. 이걸 빠뜨리면 그 조회만 실패합니다.

---

## 연결이 안 될 때 확인 순서

1. **Claude 데스크탑을 완전히 껐다 켰습니까?** — 설정을 바꾸면 재시작해야 반영됩니다
2. **새 대화를 열었습니까?** — 열려 있던 대화에서는 새 MCP가 안 잡힙니다
3. **채팅창 아래 `+` → `커넥터`** 에 그 이름이 보입니까?
4. **키를 붙여넣을 때 앞뒤 공백이나 줄바꿈이 섞이지 않았습니까?** — 가장 흔한 원인입니다
5. **JSON 콤마** — 서버 블록 사이에 콤마 하나가 빠지면 **전체가 깨집니다**

그래도 안 되면 강사에게 **화면 그대로** 보여주세요. 오류 메시지가 원인을 말해 줍니다.

> 화면을 보여줄 때 **인증키 부분은 가리세요.** 남이 보면 그대로 쓸 수 있습니다.

---

## 이 네 개로 못 하는 것

솔직히 적어둡니다.

| 못 하는 것 | 대안 |
|---|---|
| 인근 **낙찰 통계** 조회 | 낙찰 계수는 `auction-bid-price` 스킬 안에 값으로 들어 있습니다. 입찰가 산출은 됩니다 |
| 판례 심화 검색 | `korean-law` 로 상당 부분 대체됩니다 |
| 법인 채무자 회생·파산 확인 | 필요해지면 나중에 3종을 추가합니다 |
