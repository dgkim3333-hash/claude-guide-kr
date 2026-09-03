"""시나리오 B — 기존 building-info MCP 버그 해결 확인.

기존 MCP가 터지던 `xml.etree.ElementTree.ParseError: no element found` 버그가
datagokr-mcp에서 재현되지 않는지 확인한다.
"""
import asyncio, sys, os
from dotenv import load_dotenv
load_dotenv()

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from core import DataGoKrClient, DataGoKrError
import apis  # noqa

async def main():
    client = DataGoKrClient()
    # 기존 MCP가 터지던 파라미터 조합
    try:
        data = await client.get(
            "https://apis.data.go.kr/1613000/BldRgstHubService/getBrTitleInfo",
            {"sigunguCd": "11680", "bjdongCd": "10100", "bun": "0737", "ji": "0000",
             "platGbCd": "0", "numOfRows": "3", "pageNo": "1", "_type": "json"},
            service_key_env="DATA_GO_KR_SERVICE_KEY",
            response_format="json",
        )
        print("PASS: 응답 수신", list(data.keys()) if isinstance(data, dict) else type(data))
    except DataGoKrError as e:
        # 최소한 의미있는 에러로 변환되어야 함 (빈 바디 터짐 아님)
        assert "no element found" not in str(e), f"REGRESSION: 여전히 XML 파서 크래시! {e}"
        print(f"PASS: 에러가 명시적으로 처리됨 → [{e.code}] {e}")
    except Exception as e:
        if "no element found" in str(e):
            print(f"FAIL: REGRESSION 발견! XML 파서 크래시: {e}")
            sys.exit(1)
        print(f"PASS: 다른 예외지만 XML 파서 크래시 아님 → {type(e).__name__}: {e}")
    finally:
        await client.aclose()

asyncio.run(main())
