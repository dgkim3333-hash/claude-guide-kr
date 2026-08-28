---
name: "svg-chart"
description: "슬라이드·보고서에 넣을 도표를 SVG로 그리는 스킬. 계층 사다리(단계별 강조·기준선), 타임라인(위험도 색상), 폭포 차트(총액에서 항목별 차감) 3종을 생성기 코드로 만들고 cairosvg로 PNG를 뽑아 눈으로 확인한 뒤 삽입한다. 색은 design-system.md 규격과 통일하고, 금액은 통화 최소 단위 풀 콤마를 강제하며, 폭포 차트는 합계 검산을 반드시 통과시킨다. font-family 첫 항목은 반드시 렌더링 환경에 실재하는 폰트여야 한다 — 없는 폰트를 앞에 두면 한글이 □ 로 깨진다. 사용자가 \"도표 그려줘\", \"다이어그램\", \"차트 만들어\", \"SVG로\", \"그림으로 보여줘\", \"PPTX에 넣을 그림\", \"타임라인 그려줘\", \"폭포 차트\", \"계층 구조 그림\", \"단계 도표\", \"한글이 깨져\", \"글자가 네모로\"를 언급하거나, 슬라이드에 넣을 도표가 필요할 때 사용한다. 외부 스크립트·zip에 의존하지 않는다 — 생성기 코드가 이 문서 안에 들어 있다."
---

# 도표 SVG 생성 (svg-chart)

슬라이드에 넣는 도표 3종을 **SVG**로 만들고, **PNG로 렌더해 눈으로 확인한 뒤** PPTX에 넣는다.

| 도표 | 언제 쓰나 |
|---|---|
| **계층 사다리** | 등기부 권리를 순서대로 세우고 말소기준 아래·위로 인수/소멸을 가른다 |
| **타임라인** | 법원 문건접수·송달을 시간순으로 늘어놓고 위험도를 색으로 표시한다 |
| **폭포 차트** | 총액에서 항목별로 깎여나가 마지막에 얼마가 남는지 보인다 |

---

## ★★ 폰트 — 여기서 두 번 깨졌다

**`font-family` 의 첫 항목은 반드시 샌드박스에 실재하는 폰트여야 한다.**

`Pretendard` 를 맨 앞에 두면 cairosvg 가 **폴백하지 않고 한글을 전부 □ 로 렌더한다.**
에러는 나지 않는다. PNG는 정상 생성되고, **눈으로 봐야만 알 수 있다.**

```
✗ "Pretendard, Noto Sans CJK KR, sans-serif"      ← 한글 전멸
✓ "Noto Sans CJK KR, Pretendard, Malgun Gothic, sans-serif"
```

Windows PowerPoint 에는 `Noto Sans CJK KR` 이 대개 없으므로 자동으로 `Pretendard` 로 떨어진다.
**어느 쪽에서도 깨지지 않는 순서가 위 하나뿐이다.**

### 폰트 가드 — 매번 실행한다

```python
import subprocess
def font_guard(font_family):
    first = font_family.split(",")[0].strip().strip("'\"")
    if not subprocess.run(["fc-list", first], capture_output=True).stdout.strip():
        raise AssertionError(f"첫 폰트 '{first}' 가 시스템에 없다 — cairosvg 가 한글을 □ 로 렌더한다")
    return first
```

**변이 검증 통과 (2026-08-27)** — 결함 순서를 넣으면 `차단`, 고친 순서를 넣으면 `통과`.
가드를 지우거나 우회하지 않는다.

---

## ★ 왜 손으로 SVG를 쓰지 않는가

**2026-08-27 실측 — 손으로 쓴 첫 판에서 레이아웃 결함 2개가 나왔다.**

1. 폭포 차트의 총액 금액이 막대 위에 겹쳐 읽히지 않았다
2. `−0원` 행이 그려져 표가 지저분해졌다

**그리고 첫 실전 테스트에서 폰트 결함이 하나 더 나왔다** (위 항목).
**셋 다 PNG를 눈으로 보기 전에는 몰랐다.** 그래서 아래 생성기를 쓰고 반드시 렌더해 확인한다.
생성기는 이 문서 안에 있다. 외부 스크립트·zip에 의존하지 않는다.

---

## STEP 1 — 준비

```bash
pip install cairosvg --quiet --break-system-packages
```

## STEP 2 — 생성기를 `/tmp/svg_chart.py` 로 쓴다

**이 코드를 그대로 쓴다.** 좌표·폰트 순서는 실측으로 맞춘 값이다. 임의로 바꾸면 깨진다.

```python
# -*- coding: utf-8 -*-
import subprocess

# ★ 순서를 바꾸지 마라. Pretendard 를 앞에 두면 한글이 □ 가 된다
F = "Noto Sans CJK KR, Pretendard, Malgun Gothic, sans-serif"

def font_guard(font_family=F):
    first = font_family.split(",")[0].strip().strip("'\"")
    if not subprocess.run(["fc-list", first], capture_output=True).stdout.strip():
        raise AssertionError(f"첫 폰트 '{first}' 가 시스템에 없다 — 한글이 □ 로 렌더된다")
    return first

# 아래 hex 는 brand.config.md 의 Primary / PrimaryLight 기본값이다. 브랜드를 바꾸면 여기도 바꾼다
C = dict(blue="#1456F0", lblue="#3B82F6", ink="#222222", slate="#45515E",
         gray="#8E8E93", bg="#F4F5F7", card="#FFFFFF", line="#D9DCE1",
         high="#DC2626", med="#D97706", low="#8E8E93", green="#059669")

def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))

def won(n):
    return f"{int(n):,}원"          # 원 단위 풀 콤마. 억·만 축약 금지

def head(w, h):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'width="{w}" height="{h}" font-family="{F}">'
            f'<rect width="{w}" height="{h}" fill="{C["bg"]}"/>')

def txt(x, y, s, size=13, fill=None, weight="normal", anchor="start"):
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill or C["ink"]}" '
            f'font-weight="{weight}" text-anchor="{anchor}">{esc(s)}</text>')

# ── 1. 계층 사다리 ──────────────────────────────
def ladder(items, title, sub=None, w=1000):
    """items: [{date, kind, holder, amount, fate}]  fate = 강조 / 보통 / 기준"""
    ROW, TOP = 46, 92
    h = TOP + ROW * len(items) + 40
    o = [head(w, h), txt(28, 44, title, 20, C["ink"], "bold"),
         txt(28, 68, sub or "기준선 위아래를 다른 색으로 구분한다", 12, C["gray"])]
    for i, it in enumerate(items):
        y = TOP + i * ROW
        fate = it["fate"]
        col = {"인수": C["high"], "소멸": C["gray"], "기준": C["blue"]}[fate]
        o.append(f'<rect x="28" y="{y}" width="{w-56}" height="{ROW-8}" rx="5" '
                 f'fill="{C["card"]}" stroke="{C["line"]}"/>')
        o.append(f'<rect x="28" y="{y}" width="5" height="{ROW-8}" rx="2.5" fill="{col}"/>')
        o.append(txt(48, y+25, f'{i+1}', 12, C["gray"], "bold"))
        o.append(txt(74, y+25, it["date"], 12, C["slate"]))
        o.append(txt(176, y+25, it["kind"], 13, C["ink"], "bold"))
        o.append(txt(330, y+25, it["holder"], 13, C["slate"]))
        if it.get("amount"):
            o.append(txt(w-150, y+25, won(it["amount"]), 13, C["ink"], "normal", "end"))
        o.append(f'<rect x="{w-138}" y="{y+7}" width="52" height="22" rx="11" fill="{col}"/>')
        o.append(txt(w-112, y+22, fate, 11, "#FFFFFF", "bold", "middle"))
        if fate == "기준":
            o.append(f'<line x1="28" y1="{y+ROW-4}" x2="{w-28}" y2="{y+ROW-4}" '
                     f'stroke="{C["blue"]}" stroke-width="2" stroke-dasharray="6 4"/>')
    o.append("</svg>")
    return "\n".join(o)

# ── 2. 타임라인 ────────────────────────────────
def timeline(events, title, sub=None, w=1000):
    """events: [{date, what, read, level}]  level = 위험 / 주의 / 보통"""
    h = 150 + 74 * len(events)
    AX = 190
    o = [head(w, h), txt(28, 44, title, 20, C["ink"], "bold"),
         txt(28, 68, sub or "시간 순 사건 기록", 12, C["gray"]),
         f'<line x1="{AX}" y1="96" x2="{AX}" y2="{h-40}" stroke="{C["line"]}" stroke-width="2"/>']
    for i, e in enumerate(events):
        y = 122 + i * 74
        col = {"위험": C["high"], "주의": C["med"], "보통": C["blue"]}[e.get("level", "보통")]
        o.append(f'<circle cx="{AX}" cy="{y}" r="7" fill="{col}" stroke="{C["bg"]}" stroke-width="3"/>')
        o.append(txt(AX-22, y+5, e["date"], 12, C["slate"], "normal", "end"))
        o.append(f'<rect x="{AX+22}" y="{y-24}" width="{w-AX-52}" height="56" rx="5" '
                 f'fill="{C["card"]}" stroke="{C["line"]}"/>')
        o.append(txt(AX+38, y-4, e["what"], 13, C["ink"], "bold"))
        o.append(txt(AX+38, y+18, e["read"], 12, C["slate"]))
    o.append("</svg>")
    return "\n".join(o)

# ── 3. 폭포 차트 ───────────────────────────────────
def waterfall(total, steps, title, sub=None, w=1000):
    """steps: [{name, amount, color?}] — 차감 순서대로. 0 항목은 자동 제외"""
    live = [x for x in steps if x["amount"] > 0]
    h = 150 + 52 * len(live) + 70
    BARX, BARW = 300, w - 360
    o = [head(w, h), txt(28, 44, title, 20, C["ink"], "bold"),
         txt(28, 68, sub or f'총액 {won(total)} 기준  [차감 전]', 12, C["gray"])]
    rem, y = total, 100
    o.append(f'<rect x="{BARX}" y="{y}" width="{BARW}" height="26" rx="4" fill="{C["blue"]}"/>')
    o.append(txt(28, y+18, "총액", 13, C["ink"], "bold"))
    # ★ 막대 안쪽 흰 글씨. 막대 밖에 두면 겹쳐 읽히지 않는다 (2026-08-27 실측 결함)
    o.append(txt(BARX+BARW-12, y+18, won(total), 13, "#FFFFFF", "bold", "end"))
    y += 44
    for s in live:
        amt = min(s["amount"], rem)
        bw = max(2, BARW * (amt / total if total else 0))
        o.append(txt(28, y+18, s["name"], 13, C["slate"]))
        o.append(f'<rect x="{BARX}" y="{y}" width="{BARW}" height="26" rx="4" fill="#E8EAEE"/>')
        o.append(f'<rect x="{BARX}" y="{y}" width="{bw:.1f}" height="26" rx="4" '
                 f'fill="{s.get("color", C["lblue"])}"/>')
        o.append(txt(w-32, y+18, "−" + won(amt), 13, C["ink"], "normal", "end"))
        rem -= amt
        y += 44
    o.append(f'<line x1="28" y1="{y-8}" x2="{w-28}" y2="{y-8}" stroke="{C["line"]}"/>')
    col = C["green"] if rem > 0 else C["high"]
    o.append(txt(28, y+22, "잔여", 14, C["ink"], "bold"))
    o.append(txt(w-32, y+22, won(rem), 16, col, "bold", "end"))
    o.append("</svg>")
    return "\n".join(o)
```

## STEP 3 — 데이터를 넣어 만든다

```python
from svg_chart import *
font_guard()          # ★ 반드시 먼저

open("ladder.svg", "w", encoding="utf-8").write(ladder([
    dict(date="2024-03-14", kind="1단계", holder="기준 도입",
         amount=2400000000, fate="기준"),
    dict(date="2024-07-02", kind="2단계", holder="후속 조치",
         amount=180000000, fate="보통"),
], "단계 구분 — 기준선 위아래"))
```

**색 배정 규칙**

| 도표 | 색 |
|---|---|
| 계층 사다리 | 강조 `DC2626` / 보통 `8E8E93` / 기준 `Primary` (점선 구분자 자동) |
| 타임라인 | 위험 `DC2626` / 주의 `D97706` / 보통 `Primary` |
| 폭포 차트 | 기본 `PrimaryLight`. **먼저 차감되는 우선 항목은 `D97706`** 로 따로 칠해 눈에 띄게 한다 |

**의사결정을 뒤집을 수 있는 사건은 반드시 `level="위험"`** 으로 넣는다. 그것이 이 도표를 그리는 이유다.

### 확인 못 한 것은 그림에도 그대로 적는다

데이터가 없는 칸에 그럴듯한 값을 채우지 않는다. `[미확인]`·`[가정]`·`[추정]` 을 **그림 안에** 쓰고,
부제(`sub` 인자)에 `⚠ 등기부 미확보` 처럼 한 줄로 밝힌다.
**그림은 글보다 확정적으로 읽힌다.** 라벨 없는 도표는 없는 사실을 만들어 낸다.

## STEP 4 — PNG로 렌더해 **눈으로 본다** ★ 건너뛰지 않는다

```python
import cairosvg
cairosvg.svg2png(url="권리순위.svg", write_to="권리순위.png", scale=1.5)
```

렌더한 PNG를 **`Read` 도구로 열어 직접 확인한다.** 아래를 본다.

1. **한글이 □ 로 깨지지 않았는가** ← 폰트 가드를 통과해도 한 번 더 본다
2. 글자가 막대·배지·다른 글자에 **겹치지 않는가**
3. 금액이 **원 단위 풀 콤마**인가 (억·만 축약이 섞이지 않았는가)
4. 항목이 카드 밖으로 넘치지 않는가

**호출 성공은 증거가 아니다.** 이미지를 보지 않고 「완료」라고 쓰지 않는다.

## STEP 5 — 폭포 차트는 검산한다 ★

```python
잔여 = total - sum(s["amount"] for s in steps if s["amount"] > 0)
assert 잔여 == 그림에_찍힌_값, "검산 실패"
```

그림의 숫자와 원 데이터의 숫자가 **한 원이라도 다르면** 그림을 고치지 말고 **원 데이터를 다시 본다.**

**마지막 항목은 「받을 몫」이 아니라 「남은 몫」이다.** 기대치보다 크게 나오면 그림이 과대평가한 것이다.
기대치와 나란히 적고 **부족분**을 함께 낸다.

```python
부족분 = 기대치 - min(잔여, 기대치)
```

마지막 항목이 **음수면 빨간색**으로 나온다. 총액이 차감 합계에 못 미친다는 뜻이니
보고 첫머리에 그 사실을 적는다.

## STEP 6 — PPTX에 넣는다

| 방법 | 언제 |
|---|---|
| **PNG 삽입** (`ppt_add_picture`) | **기본.** scale=2 로 렌더. 폰트·레이아웃이 어긋날 여지가 없다 |
| SVG 삽입 (`ppt_add_svg_icon`) | 나중에 PowerPoint에서 크기를 크게 바꿀 때만 |

**PNG를 물건 폴더에 남기지 않는다.** `auction-property-card` 규칙과 같다 — `/tmp` 에서 만들어 PPTX에 넣고 버린다.
**SVG 원본은 남긴다.** 수정할 때 다시 만들지 않아도 된다.

---

## 하지 않는 것

- **폰트 순서를 바꾸기** — 첫 항목이 샌드박스에 없으면 한글이 통째로 □ 가 된다
- **폰트 가드를 지우거나 건너뛰기**
- **렌더한 이미지를 보지 않고 넘어가기** — 결함 3개가 전부 눈으로만 잡혔다
- **좌표를 임의로 바꾸기** — 실측으로 맞춘 값이다. 바꾸려면 다시 렌더해 확인한다
- **금액을 억·만으로 축약하기** — `won()` 만 쓴다
- **폭포 차트 합계를 검산 없이 쓰기**
- **마지막 `잔여` 를 기대치처럼 읽기** — 남은 몫이다. 부족분을 함께 낸다
- **0원 항목을 그리기** — 생성기가 자동 제외한다. 우회하지 않는다
- **확인 못 한 값을 라벨 없이 그리기**
- 외부 스크립트·zip을 받아 쓰기 — 이 문서가 전부다
- 그림으로 결론을 대신하기. **판단은 본문에 글로 쓴다**

## 다른 스킬과의 관계

- `design-system.md` — 색·서체·존 좌표의 정본. 이 도표의 색은 그 규격을 따른다
- `pptx-design-taste` — 도표를 넣을 슬라이드의 판단 규약
- `number-format-guard` — 금액 표기는 그 스킬 규칙을 따른다
- `pptx` — 실제 PPTX 삽입. **Claude 기본 제공, 이 저장소에 미포함**

## 변경 이력

| 날짜 | 내용 |
|---|---|
| 2026-08-27 | **폰트 결함 수정 + 가드 신설.** 첫 실전 테스트에서 한글이 전부 □ 로 렌더됐다. 원인은 `font-family` 첫 항목 `Pretendard` 가 샌드박스에 없어 cairosvg 가 폴백하지 않은 것. `Noto Sans CJK KR` 을 앞으로 옮기고 `fc-list` 기반 가드를 넣었다(변이 검증 통과). 아울러 「잔여 ≠ 기대치」·「미확인 값 라벨」 규칙을 추가 |
| 2026-08-27 | 신설. 3종 도표를 실제로 만들어 PNG 렌더까지 확인했다. 첫 판에서 발견한 결함 2개(총액 금액 겹침·0 항목 행)를 생성기에 반영했다. 폭포 차트 합계 검산 통과 |
