# PowerShell 이 안 보일 때

[← Node.js 설치로 돌아가기](03_설치_NodeJS.md#2-powershell-열기--글자로-컴퓨터에-일을-시키는-창)

---

**Windows 10 · 11 에는 「Windows PowerShell」이 처음부터 들어 있습니다**.
검색에 안 나오면 먼저 아래 방법으로 열어 보세요.

| 순서 | 할 일 | 이렇게 되면 성공 |
|---|---|---|
| **1** | 키보드에서 **Windows 키 + R** 을 함께 누릅니다 | 왼쪽 아래에 「실행」 작은 창 |
| **2** | `powershell` 이라고 치고 **Enter** | PowerShell 창이 열리고 첫 줄이 `PS` 로 시작 |

**그래도 열리지 않으면 새로 설치합니다.** Microsoft 가 무료로 배포하는 **PowerShell 7** 입니다.

[![PowerShell 받기](https://img.shields.io/badge/PowerShell_7-%EB%B0%9B%EA%B8%B0-5391FE?style=for-the-badge)](https://www.microsoft.com/store/apps/9MZ1SNWT0N5D)

| 방법 | 할 일 |
|---|---|
| **A. Microsoft Store (쉬움)** | 위 버튼 또는 **바로 가기 →** <https://www.microsoft.com/store/apps/9MZ1SNWT0N5D> → Store 화면에서 **「받기」(설치)** |
| **B. 설치 파일 직접 받기** (Store 가 막힌 회사 PC 등) | **바로 가기 →** <https://github.com/PowerShell/PowerShell/releases/download/v7.6.6/PowerShell-7.6.6-win-x64.msi> → 받은 `.msi` 를 더블클릭 → 선택지는 **기본값 그대로** 다음 |

설치가 끝나면 시작 메뉴에서 **PowerShell 7** 을 찾아 엽니다(검색창에 `powershell` 또는 `pwsh`).
첫 줄이 `PS` 로 시작하면 성공이고, **이 교재의 명령은 그대로 쓰시면 됩니다.** Windows PowerShell(5.1)과 PowerShell 7 은 이 교재 범위에서 문법이 같습니다.

> B 의 파일 이름에 있는 `7.6.6` 은 2026-10-01 기준 최신 판입니다. 숫자가 달라져도 Store(A)로 받으면 늘 최신이 깔립니다.

---

[← Node.js 설치로 돌아가기](03_설치_NodeJS.md#2-powershell-열기--글자로-컴퓨터에-일을-시키는-창)

출처: <https://learn.microsoft.com/ko-kr/powershell/scripting/install/install-powershell-on-windows> (2026-10-01 확인 — Windows PowerShell 5.1 기본 설치, PowerShell 7 Microsoft Store · MSI 7.6.6)
