"""
datagokr-mcp 서버 엔트리포인트.

core.registry에 등록된 ApiSpec들을 전부 읽어서
FastMCP tool로 동적 등록한다. stdio 트랜스포트로 Claude Desktop과 연결.

실행:
    uv run python server.py
또는:
    python server.py
"""
from __future__ import annotations

import asyncio
import inspect
import logging
import sys
from typing import Any, Optional

from fastmcp import FastMCP

from core import DataGoKrClient, DataGoKrError, all_specs
from core.registry import ApiSpec, Param

# apis 패키지를 import하면 각 모듈이 register(...) 호출 → 레지스트리 채워짐
import apis  # noqa: F401


log = logging.getLogger("datagokr-mcp")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    stream=sys.stderr,
)


mcp = FastMCP("datagokr-mcp")
_client = DataGoKrClient()


def _build_params_dict(spec: ApiSpec, kwargs: dict[str, Any]) -> dict[str, Any]:
    """tool 인자(kwargs: py_name 기준)를 data.go.kr 쿼리 파라미터(name 기준)로 변환."""
    out: dict[str, Any] = {}
    for p in spec.params:
        val = kwargs.get(p.tool_arg, None)
        if val is None or val == "":
            if p.required and p.default is None:
                raise ValueError(f"필수 파라미터 누락: {p.tool_arg}")
            val = p.default
        if val is None:
            continue
        if p.enum and str(val) not in p.enum:
            raise ValueError(
                f"{p.tool_arg}는 {p.enum} 중 하나여야 함. 받은 값: {val!r}"
            )
        out[p.name] = val
    return out


# Param.type → Python 타입 매핑 (FastMCP Pydantic 스키마 생성용)
_PY_TYPE_MAP: dict[str, type] = {
    "string": str,
    "integer": int,
    "number": float,
    "boolean": bool,
}


def _make_tool_handler(spec: ApiSpec):
    """ApiSpec → async 핸들러 함수 생성.

    FastMCP v3는 **kwargs를 거부하므로, 각 Param에 대응하는
    명시적 파라미터 시그니처를 inspect.Signature로 동적 설정한다.
    """
    async def handler(**kwargs: Any) -> dict[str, Any]:
        try:
            query = _build_params_dict(spec, kwargs)
            data = await _client.get(
                spec.endpoint,
                query,
                service_key_env=spec.service_key_env,
                service_key_param=spec.service_key_param,
                response_format=spec.response_format,
            )
            if spec.post_process:
                data = spec.post_process(data)
            return data
        except DataGoKrError as e:
            # MCP 클라이언트(Claude)에게 구조화된 에러 반환
            return {
                "error": True,
                "code": e.code,
                "message": str(e),
                "tool": spec.tool_name,
            }
        except Exception as e:
            log.exception("tool %s 실행 실패", spec.tool_name)
            return {"error": True, "message": f"{type(e).__name__}: {e}", "tool": spec.tool_name}

    # --- FastMCP v3 호환: 명시적 시그니처 부여 ---
    params: list[inspect.Parameter] = []
    annotations: dict[str, Any] = {}
    for p in spec.params:
        py_type = _PY_TYPE_MAP.get(p.type, str)
        if p.required and p.default is None:
            # 필수 파라미터: 기본값 없음
            params.append(inspect.Parameter(
                p.tool_arg,
                kind=inspect.Parameter.KEYWORD_ONLY,
                annotation=py_type,
            ))
        else:
            # 선택 파라미터: 기본값 설정 (None이면 Optional)
            default_val = p.default if p.default is not None else None
            param_type = Optional[py_type] if default_val is None else py_type
            params.append(inspect.Parameter(
                p.tool_arg,
                kind=inspect.Parameter.KEYWORD_ONLY,
                default=default_val,
                annotation=param_type,
            ))
            py_type = param_type
        annotations[p.tool_arg] = py_type

    handler.__signature__ = inspect.Signature(params, return_annotation=dict[str, Any])
    handler.__annotations__ = {**annotations, "return": dict[str, Any]}
    handler.__name__ = spec.tool_name
    handler.__qualname__ = spec.tool_name

    return handler


def _build_input_schema(spec: ApiSpec) -> dict[str, Any]:
    """FastMCP가 쓸 JSON schema 생성."""
    props: dict[str, Any] = {}
    required: list[str] = []
    type_map = {"string": "string", "integer": "integer", "number": "number", "boolean": "boolean"}
    for p in spec.params:
        schema: dict[str, Any] = {
            "type": type_map.get(p.type, "string"),
            "description": p.description or p.name,
        }
        if p.enum:
            schema["enum"] = p.enum
        if p.default is not None and not p.required:
            schema["default"] = p.default
        props[p.tool_arg] = schema
        if p.required and p.default is None:
            required.append(p.tool_arg)
    return {
        "type": "object",
        "properties": props,
        "required": required,
    }


def register_all_tools() -> int:
    """레지스트리의 모든 ApiSpec을 MCP tool로 등록. 등록 개수 반환."""
    count = 0
    for spec in all_specs():
        handler = _make_tool_handler(spec)

        # FastMCP v3: mcp.tool() 데코레이터 방식으로 등록
        mcp.tool(
            name=spec.tool_name,
            description=f"[{spec.category}] {spec.description}",
        )(handler)

        count += 1
        log.info("등록: %-40s (%s)", spec.tool_name, spec.category)
    return count


async def _main() -> None:
    n = register_all_tools()
    log.info("총 %d개 tool 등록 완료", n)
    await mcp.run_async(transport="stdio")


if __name__ == "__main__":
    try:
        asyncio.run(_main())
    except KeyboardInterrupt:
        pass
    finally:
        asyncio.run(_client.aclose())
