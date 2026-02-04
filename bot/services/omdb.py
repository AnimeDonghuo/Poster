import aiohttp
from typing import Any, Dict, Optional, List
from ..config import config
from ..utils.cache import TTLCache

OMDB_BASE = "http://www.omdbapi.com/"

cache = TTLCache(ttl=config.CACHE_TTL_SECONDS)


async def _request(params: Dict[str, Any]) -> Dict[str, Any]:
    if not config.OMDB_API_KEY:
        return {}
    params = dict(params)
    params["apikey"] = config.OMDB_API_KEY
    key = f"omdb:{sorted(params.items())}"
    cached = cache.get(key)
    if cached is not None:
        return cached
    timeout = aiohttp.ClientTimeout(total=config.REQUEST_TIMEOUT)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(OMDB_BASE, params=params) as resp:
            if resp.status != 200:
                return {}
            data = await resp.json()
            cache.set(key, data)
            return data


async def find_by_title(title: str, year: Optional[int] = None) -> Optional[Dict[str, Any]]:
    params: Dict[str, Any] = {"t": title}
    if year:
        params["y"] = str(year)
    data = await _request(params)
    if not data or data.get("Response") != "True":
        return None
    return data


async def search_by_title(title: str) -> List[Dict[str, Any]]:
    params: Dict[str, Any] = {"s": title}
    data = await _request(params)
    if not data or data.get("Response") != "True":
        return []
    return data.get("Search") or []
