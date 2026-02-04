import aiohttp
from typing import Any, Dict, List
from ..config import config
from ..utils.cache import TTLCache

cache = TTLCache(ttl=config.CACHE_TTL_SECONDS)


async def _fetch_json(url: str, params: Dict[str, Any] | None = None, headers: Dict[str, str] | None = None):
    key = f"json:{url}:{sorted((params or {}).items())}"
    cached = cache.get(key)
    if cached is not None:
        return cached
    timeout = aiohttp.ClientTimeout(total=config.REQUEST_TIMEOUT)
    async with aiohttp.ClientSession(timeout=timeout, headers=headers) as session:
        async with session.get(url, params=params) as resp:
            if resp.status != 200:
                return None
            data = await resp.json()
            cache.set(key, data)
            return data


async def _fetch_html(url: str, params: Dict[str, Any] | None = None, headers: Dict[str, str] | None = None) -> str:
    key = f"html:{url}:{sorted((params or {}).items())}"
    cached = cache.get(key)
    if cached is not None:
        return cached
    timeout = aiohttp.ClientTimeout(total=config.REQUEST_TIMEOUT)
    async with aiohttp.ClientSession(timeout=timeout, headers=headers) as session:
        async with session.get(url, params=params) as resp:
            if resp.status != 200:
                return ""
            text = await resp.text()
            cache.set(key, text)
            return text


async def scrape_fanart(title: str) -> List[Dict[str, Any]]:
    # FanArt.tv does not offer free API for arbitrary search, so we do a simple Google-like scrape of cached images that reference fanart.tv
    query = f"{title} site:fanart.tv"
    return await scrape_google_images(query, tag="fanart")


async def scrape_theposterdb(title: str) -> List[Dict[str, Any]]:
    query = f"{title} site:theposterdb.com"
    return await scrape_google_images(query, tag="theposterdb")


async def scrape_tvdb(title: str) -> List[Dict[str, Any]]:
    query = f"{title} site:thetvdb.com"
    return await scrape_google_images(query, tag="tvdb")


async def scrape_anidb(title: str) -> List[Dict[str, Any]]:
    query = f"{title} site:anidb.net"
    return await scrape_google_images(query, tag="anidb")


async def scrape_mal(title: str) -> List[Dict[str, Any]]:
    query = f"{title} site:myanimelist.net"
    return await scrape_google_images(query, tag="mal")


async def scrape_alphacoders(title: str) -> List[Dict[str, Any]]:
    query = f"{title} site:alphacoders.com"
    return await scrape_google_images(query, tag="alphacoders")


async def scrape_wallhaven(title: str) -> List[Dict[str, Any]]:
    query = f"{title} site:wallhaven.cc"
    return await scrape_google_images(query, tag="wallhaven")


async def scrape_cinematerial(title: str) -> List[Dict[str, Any]]:
    query = f"{title} site:cinematerial.com"
    return await scrape_google_images(query, tag="cinematerial")


async def scrape_movieposterdb(title: str) -> List[Dict[str, Any]]:
    query = f"{title} site:movieposterdb.com"
    return await scrape_google_images(query, tag="movieposterdb")


async def scrape_wikimedia(title: str) -> List[Dict[str, Any]]:
    query = f"{title} site:upload.wikimedia.org"
    return await scrape_google_images(query, tag="wikimedia")


async def scrape_google_images(query: str, tag: str = "google") -> List[Dict[str, Any]]:
    # Simple HTML scraping of thumbnails
    params = {"q": query, "tbm": "isch"}
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64)",
        "Accept-Language": "en-US,en;q=0.8",
    }
    html = await _fetch_html("https://www.google.com/search", params=params, headers=headers)
    import re

    pattern = r"https://[^"']+?.(?:jpg|jpeg|png)"
    items: List[Dict[str, Any]] = []
    for m in re.finditer(pattern, html):
        url = m.group(0)
        if "gstatic" not in url:
            items.append(
                {
                    "url": url,
                    "type": "poster",
                    "width": None,
                    "height": None,
                    "popularity": 1,
                    "clean": False,
                    "source": tag,
                }
            )
    return items


async def scrape_bing_images(query: str) -> List[Dict[str, Any]]:
    params = {"q": query}
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64)",
        "Accept-Language": "en-US,en;q=0.8",
    }
    html = await _fetch_html("https://www.bing.com/images/search", params=params, headers=headers)
    import re

    pattern = r"https://[^"']+?.(?:jpg|jpeg|png)"
    items: List[Dict[str, Any]] = []
    for m in re.finditer(pattern, html):
        url = m.group(0)
        if "mm.bing.net" not in url:
            items.append(
                {
                    "url": url,
                    "type": "poster",
                    "width": None,
                    "height": None,
                    "popularity": 1,
                    "clean": False,
                    "source": "bing",
                }
            )
    return items
