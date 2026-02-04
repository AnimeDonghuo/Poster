import aiohttp
from typing import Any, Dict, List, Optional, Literal
from ..config import config
from ..utils.cache import TTLCache
from ..utils.helpers import safe_get

TMDB_BASE = "https://api.themoviedb.org/3"
IMAGE_BASE = "https://image.tmdb.org/t/p/original"

cache = TTLCache(ttl=config.CACHE_TTL_SECONDS)


async def _request(path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    if not config.TMDB_API_KEY:
        return {}
    params = params or {}
    params["api_key"] = config.TMDB_API_KEY
    params.setdefault("language", config.DEFAULT_LANGUAGE)
    url = f"{TMDB_BASE}{path}"
    key = f"tmdb:{url}:{sorted(params.items())}"
    cached = cache.get(key)
    if cached is not None:
        return cached
    timeout = aiohttp.ClientTimeout(total=config.REQUEST_TIMEOUT)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(url, params=params) as resp:
            if resp.status != 200:
                return {}
            data = await resp.json()
            cache.set(key, data)
            return data


async def search_multi(query: str, year: Optional[int] = None) -> List[Dict[str, Any]]:
    params: Dict[str, Any] = {"query": query}
    if year:
        params["year"] = year
    data = await _request("/search/multi", params)
    return data.get("results") or []


async def search_collection(query: str) -> List[Dict[str, Any]]:
    data = await _request("/search/collection", {"query": query})
    return data.get("results") or []


async def search_tv(query: str) -> List[Dict[str, Any]]:
    data = await _request("/search/tv", {"query": query})
    return data.get("results") or []


async def search_movie(query: str, year: Optional[int] = None) -> List[Dict[str, Any]]:
    params: Dict[str, Any] = {"query": query}
    if year:
        params["year"] = year
    data = await _request("/search/movie", params)
    return data.get("results") or []


async def get_details(media_type: Literal["movie", "tv"], tmdb_id: int) -> Dict[str, Any]:
    return await _request(f"/{media_type}/{tmdb_id}")


async def get_trending(media_type: Literal["movie", "tv"], time_window: str = "day") -> List[Dict[str, Any]]:
    data = await _request(f"/trending/{media_type}/{time_window}")
    return data.get("results") or []


async def get_images(media_type: Literal["movie", "tv"], tmdb_id: int) -> Dict[str, Any]:
    return await _request(f"/{media_type}/{tmdb_id}/images")


def build_image_items(images: Dict[str, Any]) -> List[Dict[str, Any]]:
    posters = safe_get(images, "posters", default=[]) or []
    backdrops = safe_get(images, "backdrops", default=[]) or []

    items = []
    for p in posters:
        path = p.get("file_path")
        if not path:
            continue
        items.append(
            {
                "url": f"{IMAGE_BASE}{path}",
                "type": "poster",
                "width": p.get("width"),
                "height": p.get("height"),
                "popularity": p.get("vote_count"),
                "clean": True,
            }
        )
    for b in backdrops:
        path = b.get("file_path")
        if not path:
            continue
        items.append(
            {
                "url": f"{IMAGE_BASE}{path}",
                "type": "backdrop",
                "width": b.get("width"),
                "height": b.get("height"),
                "popularity": b.get("vote_count"),
                "clean": True,
            }
        )
    return items
