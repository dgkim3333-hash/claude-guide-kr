# 03-1 · Node.js 설치

[← 03 사전 준비 프로그램으로 돌아가기](03_사전준비프로그램.md#설치--nodejs--uv--vs-code--git)

---

> 섹션 05 에서 설정 파일의 `"command": "npx"` 로 띄우는 MCP 에 필요합니다.
> 이게 없으면 그 MCP 는 설정 파일을 아무리 잘 넣어도 나타나지 않습니다.

## 1. 받기

[![Node.js 받기](https://img.shields.io/badge/Node.js-%EB%B0%9B%EA%B8%B0-339933?style=for-the-badge)](https://nodejs.org/ko/download)

```
https://nodejs.org/ko/download
```

페이지가 열리면 **위쪽 명령어 상자는 건너뛰고, 아래쪽 초록 버튼만** 씁니다.

| 순서 | 할 일 | 이렇게 되면 성공 |
|---|---|---|
| **1** | 맨 위 줄 `Node.js® v24.21.0 LTS` 처럼 버전 옆에 **LTS** 가 붙어 있는지 확인합니다 | 파란 `LTS` 표시가 보임 (숫자는 달라질 수 있습니다) |
| **2** | 가운데 **명령어 상자(Docker · npm)는 무시**합니다. 우리는 쓰지 않습니다 | — |
| **3** | 아래 「또는 **x64** 아키텍처가 실행 중인 **Windows** 환경에서…」 줄 바로 밑의 초록 버튼 **「Windows 설치 프로그램 (.msi)」** 을 누릅니다 | 다운로드 폴더에 `node-v24…-x64.msi` 파일 |
| **4** | 받은 `.msi` 파일을 더블클릭해 설치합니다. 선택지는 **전부 기본값 그대로** 두고 다음만 누릅니다 | 「Completed」 화면 |

> [!WARNING]
> 옆의 **「Standalone Binary (.zip)」 는 누르지 마세요.** 압축 파일이라 설치가 되지 않습니다.
> 대부분의 PC 는 `x64` 그대로 두면 됩니다. 노트북이 ARM 칩(일부 Surface 등)이면 `x64` 칸을 눌러 `ARM64` 로 바꾸세요.

## ★ 체크박스 하나만 조심하세요 — 여기서 30분이 날아갑니다

설치가 거의 끝날 무렵 이런 체크박스가 나옵니다.

```
Automatically install the necessary tools for Native Modules
```

**체크하지 마세요.** 기본값(꺼짐) 그대로 두고 넘어가시면 됩니다.

「필요한 도구(necessary tools)」라고 적혀 있어서 켜야 할 것 같지만, **이 교육에는 필요 없습니다.**
C나 C++로 만든 프로그램을 내 컴퓨터에서 직접 번역(컴파일)할 때 쓰는 개발자용 도구입니다.
우리가 붙이는 MCP 는 전부 이미 만들어진 것을 받아서 실행하므로 번역할 일이 없습니다.

체크하면 설치가 끝난 뒤 **검은 창이 나오면서** 이런 문구가 나옵니다.

```
This script will install Python and the Visual Studio Build Tools...
This will require about 7 GiB of free disk space...
```

**파이썬 · 비주얼 스튜디오 빌드 도구 · Chocolatey · 윈도우 업데이트**를 전부 깔기 시작합니다.
디스크 7GB 이상을 쓰고 수십 분이 걸리며, 재부팅을 요구하기도 합니다.

### 이미 그 검은 창을 보셨다면

**그냥 창을 닫으세요.** 화면 아래쪽에도 `You can close this window to stop now` 라고 적혀 있습니다.
**Node.js 자체는 이미 설치가 끝난 상태**입니다. 이건 덤으로 딸려 나온 별개 스크립트일 뿐입니다.

중간에 닫아도 컴퓨터에 문제가 생기지 않습니다. 이미 다 깔렸더라도 해로운 것은 아니고
공간만 차지합니다. 정리하고 싶으시면 `설정 → 앱` 에서 **Chocolatey** 와
**Visual Studio Build Tools** 를 지우시면 됩니다.

## 2. 설치 확인

**PowerShell 창을 닫고 새로 연 다음** 아래 한 줄을 넣습니다.

```powershell
node -v
```

`v24.21.0` 처럼 버전 번호가 나오면 성공입니다.

> **★ `v22` 보다 낮게 나오면 다시 까셔야 합니다.**
> 예전에 깔아둔 Node.js 가 있으면 낮은 버전이 그대로 남아 있을 수 있습니다.
> 수업에서 붙이는 **Firecrawl 은 Node.js 22 이상**을 요구합니다 (`firecrawl-mcp` 3.24.0 기준).
> `v20` 이나 `v18` 이 나오면 위 1번으로 돌아가 **「Windows 설치 프로그램 (.msi)」** 으로 다시 설치하십시오. 덮어써집니다.

## 3. Claude 데스크탑 다시 켜기

Node.js 를 새로 깔았다면 **Claude 데스크탑을 완전히 종료했다가 다시 켜야** 인식합니다.
창만 닫으면 뒤에서 계속 돌고 있습니다. 작업 표시줄 우측 트레이 아이콘까지 종료하세요.

---

[← 03 사전 준비 프로그램으로 돌아가기](03_사전준비프로그램.md#설치--nodejs--uv--vs-code--git)

출처: <https://nodejs.org/ko/download> (2026-10-01 확인 — 현재 LTS v24.21.0, 화면 구성: 위쪽 명령어 상자 + 아래쪽 「Windows 설치 프로그램 (.msi)」 버튼)
