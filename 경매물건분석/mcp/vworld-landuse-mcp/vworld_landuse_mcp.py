import os, json, httpx
from mcp.server.fastmcp import FastMCP

API_KEY = os.environ.get("VWORLD_API_KEY", "").strip()
DOMAIN = os.environ.get("VWORLD_DOMAIN", "").strip()
LAYERS = [s.strip() for s in os.environ.get(
    "VWORLD_LANDUSE_LAYERS",
    "LT_C_UQ111,LT_C_UQ112,LT_C_UQ113,LT_C_UQ114").split(",") if s.strip()]

GEO = "https://api.vworld.kr/req/address"
DATA = "https://api.vworld.kr/req/data"
PARCEL = "LP_PA_CBND_BUBUN"

mcp = FastMCP("vworld-landuse")

def _get(url, params):
    params = dict(params); params["key"] = API_KEY; params.setdefault("format", "json")
    if DOMAIN: params["domain"] = DOMAIN
    with httpx.Client(timeout=20.0) as c:
        r = c.get(url, params=params); r.raise_for_status()
        t = r.text.strip()
        try: return json.loads(t)
        except json.JSONDecodeError: return {"_raw": t[:2000]}

def _geocode(address):
    last = None
    for at in ("PARCEL", "ROAD"):
        res = _get(GEO, {"service": "address", "request": "getcoord",
                         "crs": "epsg:4326", "address": address, "type": at})
        last = res
        if (res.get("response", {}) or {}).get("status") == "OK":
            p = res["response"]["result"]["point"]
            return {"x": float(p["x"]), "y": float(p["y"]), "type": at}
    return {"error": "geocode_failed", "address": address, "raw": last}

def _point(layer, x, y, size=10, geometry=False):
    return _get(DATA, {"service": "data", "request": "GetFeature", "data": layer,
                       "crs": "EPSG:4326", "geomFilter": f"POINT({x} {y})",
                       "geometry": "true" if geometry else "false", "size": str(size)})

def _feats(res):
    try: return res["response"]["result"]["featureCollection"]["features"] or []
    except Exception: return []

def _need():
    return None if API_KEY else {"error": "VWORLD_API_KEY not set in config env."}

@mcp.tool()
def server_config() -> dict:
    """Show server config status (key value not exposed)."""
    return {"api_key_set": bool(API_KEY), "domain": DOMAIN or "(none)", "landuse_layers": LAYERS}

@mcp.tool()
def geocode_address(address: str) -> dict:
    """Convert an address to lon/lat. Tries jibun then road address."""
    return _need() or _geocode(address)

@mcp.tool()
def get_parcel_info(address: str = "", pnu: str = "") -> dict:
    """Parcel info: PNU, jibun, addr, individual land price (jiga). Give address or pnu."""
    e = _need()
    if e: return e
    if pnu:
        res = _get(DATA, {"service": "data", "request": "GetFeature", "data": PARCEL,
                          "attrFilter": f"pnu:=:{pnu}", "geometry": "false", "size": "5"})
        f = _feats(res)
        return {"source": "pnu", "count": len(f), "parcels": [x.get("properties", {}) for x in f]}
    if address:
        g = _geocode(address)
        if "error" in g: return g
        f = _feats(_point(PARCEL, g["x"], g["y"], size=5))
        return {"source": "address", "geocode": g, "count": len(f),
                "parcels": [x.get("properties", {}) for x in f]}
    return {"error": "give address or pnu"}

@mcp.tool()
def get_land_use_plan(address: str = "") -> dict:
    """Land-use plan (zoning) for an address. Core tool for NPL land analysis."""
    e = _need()
    if e: return e
    if not address: return {"error": "address required"}
    g = _geocode(address)
    if "error" in g: return g
    x, y = g["x"], g["y"]
    parcel = [f.get("properties", {}) for f in _feats(_point(PARCEL, x, y, size=3))]
    zoning = []
    for layer in LAYERS:
        try:
            f = _feats(_point(layer, x, y, size=10))
            if f: zoning.append({"layer": layer, "count": len(f),
                                 "properties": [z.get("properties", {}) for z in f]})
        except Exception as ex:
            zoning.append({"layer": layer, "error": str(ex)})
    return {"geocode": g, "parcel": parcel[0] if parcel else None,
            "layers_queried": LAYERS, "zoning": zoning,
            "note": "If zoning is empty, layer IDs are wrong. Use probe_layer to find correct ones."}

@mcp.tool()
def probe_layer(layer_id: str, address: str) -> dict:
    """Test whether a VWorld layer ID returns data at an address (to confirm correct zoning IDs)."""
    e = _need()
    if e: return e
    g = _geocode(address)
    if "error" in g: return g
    f = _feats(_point(layer_id, g["x"], g["y"], size=10))
    return {"layer_id": layer_id, "geocode": g, "feature_count": len(f),
            "sample_properties": f[0].get("properties", {}) if f else None, "works": bool(f)}

if __name__ == "__main__":
    mcp.run()
