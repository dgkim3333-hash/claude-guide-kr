# 03-4 · Git 설치

[← 03 사전 준비 프로그램으로 돌아가기](03_사전준비프로그램.md#설치--nodejs--uv--vs-code--git)

---

> 📄 교재 PDF **p.23** — 미리 깔아두면 좋은 프로그램
>
> 데스크탑 앱의 `Code` 탭을 쓰려면 필요합니다. **`Code` 탭을 안 쓰실 거면 안 깔아도 됩니다.** 채팅·Cowork·MCP 는 Git 없이 전부 됩니다.

## $\color{#d97757}{\textsf{1. 받기}}$

[![Git 받기](https://img.shields.io/badge/Git-%EB%B0%9B%EA%B8%B0-F05032?style=for-the-badge)](https://git-scm.com/install/windows)

**바로 가기 →** <https://git-scm.com/install/windows>

받아서 **계속 「다음」만 누르시면 됩니다.** 설정은 하나도 안 건드려도 됩니다.

## $\color{#d97757}{\textsf{2. Claude 데스크탑 다시 켜기}}$

깔고 나면 **Claude 데스크탑을 완전히 끄고 다시 켜세요.** 그래야 `Code` 탭이 Git 을 찾습니다.
창만 닫으면 뒤에서 계속 돌고 있습니다. 작업 표시줄 우측 트레이 아이콘까지 종료하세요.

---

## $\color{#d97757}{\textsf{Git 은 무엇이고 왜 필요한가}}$

**파일이 언제 어떻게 바뀌었는지 기록해 두는 프로그램**입니다.
사진 찍듯이 상태를 저장해 두고, 나중에 아무 시점으로나 되돌아갈 수 있게 해줍니다.
**무한 되돌리기 + 변경 장부**라고 생각하시면 됩니다.

| | Git 이 없으면 | Git 이 있으면 |
|---|---|---|
| 되돌리기 | 못 합니다 | 며칠 전 상태로도 돌아갑니다 |
| 뭐가 바뀌었나 | 모릅니다 | 바뀐 줄에 색이 칠해집니다 |

섹션 08 「Cowork 와 Code」 의 「Code 에만 있는 것 — 되돌리기가 됩니다 · 어디를 고쳤는지 보여줍니다」가
**전부 Git 덕분**입니다. 그래서 `Code` 탭이 Git 을 요구합니다.

### ★ Git 과 GitHub 는 다른 것입니다

이름이 비슷해서 가장 많이 헷갈립니다.

| | 무엇 |
|---|---|
| **Git** | 내 컴퓨터에 설치하는 **프로그램**. 혼자 돌아갑니다 |
| **GitHub** | 그 기록을 올려두는 **웹사이트**. 이 자료를 받는 그곳 |

**교재를 받으려고 GitHub 에 가입할 필요가 없듯이, Git 을 설치한다고 GitHub 를 쓰는 것도 아닙니다.**

---

[← 03 사전 준비 프로그램으로 돌아가기](03_사전준비프로그램.md#설치--nodejs--uv--vs-code--git)

출처: code.claude.com/docs/en/desktop-quickstart (2026-08-18 직접 조회) — "On Windows, Git must be installed for local sessions to work." · <https://git-scm.com/install/windows> (2026-10-01 확인 — 예전 주소 /downloads/win 은 이 주소로 넘어감)
