# 슬라이드 디자인 시스템

**Claude 에게 슬라이드를 시키면 매번 다르게 나옵니다.** 제목 위치가 밀리고, 색이 바뀌고, 어떤 장은 아래가 텅 빕니다.
이 저장소는 **좌표·색·서체를 못 박아** 매번 같게 나오게 만듭니다. 예쁜 것보다 **일정한 것**이 목적입니다.

![표지](examples/preview/01.png)
![KPI와 차트](examples/preview/02.png)
![2단 비교](examples/preview/03.png)

> 위 세 장은 `examples/build_sample_deck.py` 를 그대로 돌려 나온 결과입니다.

---

## 30분 안에 첫 덱 만들기

### 1단계 — 파일 받기 (3분)

초록색 `Code` 버튼 → `Download ZIP` → 압축을 풉니다.

### 2단계 — 프로젝트 만들기 (5분)

1. Claude 데스크탑에서 **프로젝트**를 새로 만듭니다
2. **지침 편집(커스텀 인스트럭션)** 을 엽니다
3. **`design-system.md` 를 통째로 복사해 붙여넣습니다**

이 한 번으로 존 좌표·그리드·패턴·점검표가 전부 들어갑니다.

### 3단계 — 스킬 3개 올리기 (7분)

`설정` → `사용자 지정` → `스킬` → 우측 상단 `추가` → `스킬 업로드`

아래 세 파일을 하나씩 올립니다. **`.md` 파일을 그대로 올리면 됩니다.**

| 파일 | 무엇을 하나 |
|---|---|
| `skills/pptx-design-taste/SKILL.md` | 덱 규격이 미학 규칙보다 위라고 선언한다 |
| `skills/number-format-guard/SKILL.md` | 저장 직전 숫자 표기를 검사한다 |
| `skills/svg-chart/SKILL.md` | 복잡한 도표를 SVG → PNG 로 만든다 |

올린 뒤 **새 대화**부터 적용됩니다. 1~2분 보안 검사를 거칩니다.

### 4단계 — 브랜드 바꾸기 (5분)

`brand.config.md` 를 열어 **색·서체·로고·통화**를 자기 것으로 바꿉니다.
로고는 `assets/logo-placeholder.png` 자리에 **같은 파일명으로 덮어씁니다.**

### 5단계 — 시켜보기 (10분)

프로젝트 안에서 새 대화를 열고 이렇게 말합니다.

```
이 자료로 5장짜리 덱을 만들어줘. design-system.md 규격을 지켜줘.
먼저 HTML 미리보기를 보여주고, 승인하면 pptx로 만들어줘.
```

미리보기를 보고 승인하면 .pptx 가 나옵니다.

---

## `brand.config.md` — 여기만 고칩니다

1. 색·서체·로고·통화가 **그 파일 하나에** 모여 있습니다
2. 로고는 `assets/logo-placeholder.png` 를 **같은 이름으로 덮어씁니다**
3. 서체를 바꿨다면 **발표할 PC 에도 그 서체를 설치**하세요. 없으면 PowerPoint 가 임의로 다른 글꼴을 쓰고 줄바꿈이 전부 달라집니다

---

## Claude 가 기본으로 주는 스킬 두 개

이 저장소에는 **`pptx` 와 `design-taste-frontend` 가 들어 있지 않습니다.** 받으실 필요도 없습니다.

- **`pptx`** — .pptx 파일을 읽고 쓰는 스킬. **Claude 가 기본 제공**합니다. 이 저장소가 배포하지 않는 이유는 Anthropic 라이선스가 복제·재배포·2차 저작물을 금지하기 때문입니다
- **`design-taste-frontend`** — 「AI 티 나는 디자인」을 잡아내는 스킬. 공개 저장소에 올라와 있지 않고 라이선스 표기도 없어 재배포하지 않습니다

`design-system.md` 의 스킬 로드 순서 표는 이 둘을 **부르라고** 지시합니다. 파일이 없을 뿐, 지시는 유효합니다.
혹시 `design-taste-frontend` 가 목록에 없으면 나머지만으로도 작동합니다.

---

## 폴더 구조

```
슬라이드디자인/
├─ README.md                  이 파일
├─ LICENSE                    MIT
├─ brand.config.md            ★ 수강생이 고치는 유일한 파일
├─ design-system.md           프로젝트 지침에 붙여넣을 본체 (645줄)
├─ skills/
│  ├─ pptx-design-taste/SKILL.md
│  ├─ number-format-guard/SKILL.md
│  └─ svg-chart/SKILL.md
├─ assets/
│  └─ logo-placeholder.png    교체 대상
├─ examples/
│  ├─ build_sample_deck.py    ★ 실제로 배우는 건 이 파일입니다
│  ├─ sample-deck.pptx
│  └─ preview/01~05.png
└─ docs/
   ├─ QUICKSTART.md
   └─ TROUBLESHOOTING.md
```

---

## 자주 막히는 곳

| 증상 | 원인 |
|---|---|
| 한글이 □ 로 깨진다 | SVG·PNG 를 만들 때 `font-family` 첫 항목이 그 환경에 없는 글꼴이다 |
| 장마다 제목 위치가 다르다 | 지침을 프로젝트가 아니라 대화에만 붙여넣었다 |
| 금액이 「3.5억」으로 나온다 | `number-format-guard` 를 안 올렸다 |
| 아래가 텅 빈다 | 밀도 규칙을 안 읽혔다. 「본문 상자 안에서 채우라」고 다시 말한다 |

자세한 것은 [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) 를 보세요.

---

## 라이선스

MIT. 자기 업무에 마음대로 가져다 쓰시라고 만든 것입니다. [LICENSE](LICENSE) 참조.

이 저장소는 Anthropic 제공 스킬(`pptx`, `design-taste-frontend`)을 **포함하지 않습니다.**
해당 스킬은 Claude 에서 기본 제공되며 각자의 이용약관을 따릅니다.

서체 **Pretendard** 는 이 저장소에 동봉하지 않았습니다. 필요하면 배포처에서 직접 받으세요.
