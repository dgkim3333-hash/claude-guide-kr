"""Phase 1 스모크 테스트. 핵심 5개 + 카테고리별 샘플 API가 실제로 살아있는지 확인."""
import asyncio, os, sys, json
from dotenv import load_dotenv
load_dotenv()

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from core import DataGoKrClient, DataGoKrError
import apis  # noqa: F401
from core.registry import all_specs

TEST_CASES = [
    # === Phase 1: 핵심 5개 ===
    ("epost_address_search", {"search_type": "road", "keyword": "테헤란로 152", "count_per_page": 3, "page": 1}),
    ("legal_dong_code_search", {"keyword": "강남구 역삼동", "num_of_rows": 5, "page_no": 1, "type": "json"}),
    ("building_title", {"sigungu_cd": "11680", "bjdong_cd": "10100", "bun": "0737", "ji": "0000",
                        "plat_gb_cd": "0", "num_of_rows": 3, "page_no": 1, "_type": "json"}),
    ("realprice_apt_trade", {"lawd_cd": "11680", "deal_ym": "202601", "num_of_rows": 5, "page_no": 1}),
    ("onbid_notice_list", {"num_of_rows": 5, "page_no": 1, "type": "json"}),

    # === Phase 2: 카테고리별 샘플 ===
    ("building_basis_outline", {"sigungu_cd": "11680", "bjdong_cd": "10100", "bun": "0737", "ji": "0000",
                                "plat_gb_cd": "0", "num_of_rows": 3, "page_no": 1, "_type": "json"}),
    ("realprice_officetel_trade", {"lawd_cd": "11680", "deal_ym": "202601", "num_of_rows": 5, "page_no": 1}),
    ("realprice_land_trade", {"lawd_cd": "11680", "deal_ym": "202601", "num_of_rows": 5, "page_no": 1}),
    ("onbid_realestate_list", {"num_of_rows": 5, "page_no": 1, "type": "json"}),
    ("sbiz_stores_in_radius", {"cx": 127.0495556, "cy": 37.5040537, "radius": 500, "num_of_rows": 5, "page_no": 1, "type": "json"}),
    ("apt_complex_list", {"sigungu_code": "11680", "bjdong_code": "10100", "num_of_rows": 5, "page_no": 1}),
    ("urban_rail_route", {"station_name": "강남", "num_of_rows": 5, "page_no": 1}),
]


def _build_query(spec, tool_kwargs):
    """tool kwargs (py_name 기준) → data.go.kr query params (name 기준)"""
    out = {}
    for p in spec.params:
        val = tool_kwargs.get(p.tool_arg)
        if val is None:
            val = p.default
        if val is None or val == "":
            continue
        out[p.name] = val
    return out


async def main():
    client = DataGoKrClient()
    specs_by_name = {s.tool_name: s for s in all_specs()}
    results = []

    for tool_name, kwargs in TEST_CASES:
        spec = specs_by_name[tool_name]
        try:
            query = _build_query(spec, kwargs)
            data = await client.get(
                spec.endpoint, query,
                service_key_env=spec.service_key_env,
                service_key_param=spec.service_key_param,
                response_format=spec.response_format,
            )
            if spec.post_process:
                data = spec.post_process(data)
            if isinstance(data, dict):
                items = data.get("items", [])
                item_count = len(items) if isinstance(items, list) else "?"
            else:
                item_count = "?"
            status = "OK" if item_count != 0 else "EMPTY"
            emoji = "✅" if item_count else "⚠️"
            print(f"{emoji} {tool_name}: items={item_count}")
            results.append((tool_name, status, item_count))
        except DataGoKrError as e:
            print(f"❌ {tool_name}: [{e.code}] {e}")
            results.append((tool_name, "FAIL", str(e)))
        except Exception as e:
            print(f"💥 {tool_name}: {type(e).__name__}: {e}")
            results.append((tool_name, "ERROR", str(e)))

    await client.aclose()

    print("\n=== SUMMARY ===")
    ok = sum(1 for r in results if r[1] in ("OK", "EMPTY"))
    fail = len(results) - ok
    for name, status, detail in results:
        icon = "✅" if status in ("OK", "EMPTY") else "❌"
        print(f"  {icon} {name}: {status} ({detail})")
    print(f"\n총 {len(results)}개 중 {ok}개 성공, {fail}개 실패")


asyncio.run(main())
