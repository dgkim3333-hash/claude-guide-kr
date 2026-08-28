# brand.config.md — 여기만 고치세요

이 저장소에서 **수강생이 고치는 파일은 이것 하나입니다.**
색·서체·로고·통화가 전부 여기 모여 있고, `design-system.md` 본문은 아래 토큰 이름으로만 이 값을 참조합니다.

1. 아래 값을 자기 회사 것으로 바꿉니다.
2. 로고는 `assets/logo-placeholder.png` 자리에 **같은 파일명으로 덮어씁니다.** 파일명을 바꾸면 참조가 끊깁니다.
3. 서체가 PC에 깔려 있지 않으면 PowerPoint가 임의로 다른 글꼴을 씁니다 — 줄바꿈과 폭이 전부 달라집니다. 서체를 바꿨다면 **발표할 PC에도 그 서체를 설치**하세요.

---

## 브랜드

| 토큰 | 기본값 | 설명 |
|---|---|---|
| `BrandName` | `MyBrand` | 표지·마감 슬라이드에 들어가는 이름 |
| `LogoFile` | `assets/logo-placeholder.png` | **교체 대상.** 배경이 투명한 PNG 권장 |
| `LogoSize` | 폭 약 1.22" × 높이 0.24" | 비율 고정. 높이 0.24"에 맞춰 균일 확대·축소만 |

## 서체

| 토큰 | 기본값 | 설명 |
|---|---|---|
| `BodyFont` | `Pretendard` | 이 덱에서 쓰는 **유일한** 서체. 굵기(100~900)로만 위계를 만든다 |
| `FontFallback` | `Pretendard, "Pretendard Variable", -apple-system, system-ui, sans-serif` | 내보내기 안전용 문자열 |

- Pretendard는 이 저장소에 동봉하지 않았습니다. 필요하면 배포처에서 직접 받으세요.
- 다른 서체로 바꿔도 됩니다. **단 하나만 쓰는 규칙은 그대로 지킵니다.**
- 리눅스 샌드박스에서 SVG·PNG를 뽑을 때는 `font-family` 첫 항목이 **그 환경에 실제로 있는 글꼴**이어야 합니다. 없는 글꼴을 앞에 두면 한글이 □ 로 깨집니다.

## 색

| 토큰 | 기본값 | 쓰임 |
|---|---|---|
| `Primary` | `#1456f0` | 브랜드 기본색. KPI 숫자, 주 차트 계열 |
| `PrimaryLight` | `#3b82f6` | 차트 주 계열, 강조 |
| `PrimaryLighter` | `#60a5fa` | 차트 보조, 밝은 채움 |
| `PrimaryPale` | `#bfdbfe` | 밝은 배경 |
| `PrimaryDeep` | `#2563eb` / `#1d4ed8` | 강조 / 깊은 강조 |
| `BrandDeep` | `#17437d` | 짙은 브랜드 톤 |
| `SkyBlue` | `#3daeff` | 밝은 변형 악센트 |
| `Accent` | `#ea5ec1` | **장식 전용.** 본문 글자·버튼에 쓰지 않는다 |
| `TextMain` | `#222222` | 본문·제목 |
| `TextHeadingDark` | `#18181b` | 어두운 배경 위 제목 |
| `TextSub` | `#45515e` | 부제목·캡션 |
| `TextMuted` | `#8e8e93` | 챕터명·쪽번호·출처 |
| `TextHelper` | `#5f5f5f` | 도움말 |
| `SurfaceWhite` | `#ffffff` | 모든 슬라이드 배경 |
| `SurfaceSecondary` | `#f0f0f0` | 보조 컨테이너 |
| `DarkSurface` | `#181e25` | 섹션 구분·마감 슬라이드 배경 |
| `Border` | `#e5e7eb` | 컴포넌트 테두리, 격자선 |
| `Divider` | `#f2f3f5` | 옅은 구분선 |
| `SuccessBg` / `SuccessText` | `#e8ffea` / `#16a34a` | 성공 표시 |

**색값 자체는 그대로 두셔도 됩니다.** 중립적인 파랑 계열이라 특정 브랜드가 드러나지 않습니다.
바꾸실 거면 `Primary` → `PrimaryLight` → `PrimaryLighter` 세 개를 **밝기 순서가 유지되도록** 함께 바꾸세요. Hero Gradient가 이 세 색으로 만들어집니다.

## 그라디언트

| 토큰 | 값 |
|---|---|
| `HeroGradient` | `linear-gradient(135deg, Primary 0%, PrimaryLight 50%, PrimaryLighter 100%)` |

각도 135°, 정지점 0/50/100 고정. **슬라이드당 1개, 덱 전체 3개**를 넘지 않습니다.

## 그림자

| 토큰 | 값 |
|---|---|
| `ShadowStandard` | `rgba(0,0,0,0.08) 0px 4px 6px` |
| `ShadowSoftGlow` | `rgba(0,0,0,0.08) 0px 0px 22.576px` |
| `ShadowBrandGlow` | `rgba(44,30,116,0.16) 0px 0px 15px` |
| `ShadowBrandGlowOffset` | `rgba(44,30,116,0.11) 6.5px 2px 17.5px` |
| `ShadowElevated` | `rgba(36,36,36,0.08) 0px 12px 16px -4px` |

## 숫자·통화

| 토큰 | 기본값 | 설명 |
|---|---|---|
| `Currency` | `원` | 통화 단위 표기 |
| `CurrencyStyle` | 최소 단위 + 세 자리 콤마 | 예: `1,234,567,890원`. 만/억/조 축약 금지 |

축약은 **그래프 축 라벨에서만** 허용합니다. 본문·표·KPI·데이터 라벨은 전부 풀 자리로 씁니다.
