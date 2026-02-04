from typing import Any, Dict, List, Optional, Literal
from . import tmdb
from . import omdb
from . import imdb_scraper
from . import image_scraper
from ..utils.helpers import dedupe_images, sort_images
from ..utils.cache import TTLCache
from ..config import config

cache = TTLCache(ttl=config.CACHE_TTL_SECONDS)


async def detect_content_type(query: str) -> str:
    lowered = query.lower()
    if any(k in lowered for k in ["season", "episode", "s0", "e0", "web series"]):
        return "TV Show"
    if any(k in lowered for k in ["kdrama", "k-drama"]):
        return "K-Drama"
    if any(k in lowered for k in ["donghua"]):
        return "Donghua"
    if any(k in lowered for k in ["manga"]):
        return "Manga"
    if any(k in lowered for k in ["anime"]):
        return "Anime"
    if any(k in lowered for k in ["collection", "universe", "saga"]):
        return "Collection"
    return "Movie/TV"


async def search_title(query: str, year: Optional[int] = None) -> Optional[Dict[str, Any]]:
    key = f"search:{query}:{year}"
    cached = cache.get(key)
    if cached is not None:
        return cached

    tmdb_results = await tmdb.search_multi(query, year)
    chosen: Optional[Dict[str, Any]] = None
    for r in tmdb_results:
        if r.get("media_type") in ("movie", "tv"):
            chosen = r
            break
    if not chosen:
        colls = await tmdb.search_collection(query)
        if colls:
            chosen = colls[0]

    if not chosen:
        omdb_data = await omdb.find_by_title(query, year)
        if omdb_data:
            chosen = {
                "media_type": "movie",
                "title": omdb_data.get("Title"),
                "name": omdb_data.get("Title"),
                "overview": omdb_data.get("Plot"),
                "release_date": omdb_data.get("Year"),
                "vote_average": float(omdb_data["imdbRating"])
                if omdb_data.get("imdbRating") not in (None, "N/A")
                else None,
                "genres": [
                    g.strip()
                    for g in (omdb_data.get("Genre") or "").split(",")
                    if g.strip()
                ],
                "imdb_id": omdb_data.get("imdbID"),
            }

    cache.set(key, chosen)
    return chosen


async def get_metadata_and_images(query: str, year: Optional[int] = None) -> Optional[Dict[str, Any]]:
    info = await search_title(query, year)
    if not info:
        return None

    media_type_raw = info.get("media_type") or "movie"
    if media_type_raw == "tv":
        media_type: Literal["movie", "tv"] = "tv"
    elif media_type_raw == "movie":
        media_type = "movie"
    else:
        media_type = "movie"

    tmdb_id = info.get("id")
    details: Dict[str, Any] = {}
    tmdb_images: List[Dict[str, Any]] = []

    if tmdb_id:
        details = await tmdb.get_details(media_type, tmdb_id)
        images = await tmdb.get_images(media_type, tmdb_id)
        tmdb_images = tmdb.build_image_items(images)

    title = (
        details.get("title")
        or details.get("name")
        or info.get("title")
        or info.get("name")
        or query
    )
    year_val: Optional[int] = None
    date = (
        details.get("release_date")
        or details.get("first_air_date")
        or info.get("release_date")
    )
    if date and len(date) >= 4:
        try:
            year_val = int(date[:4])
        except ValueError:
            year_val = None
    rating = details.get("vote_average") or info.get("vote_average")
    genres = (
        [g["name"] for g in details.get("genres", [])]
        if details.get("genres")
        else info.get("genres")
        or []
    )
    overview = details.get("overview") or info.get("overview") or ""
    imdb_id = details.get("imdb_id") or info.get("imdb_id")

    scraped_images: List[Dict[str, Any]] = []

    # IMDb images
    if imdb_id:
        scraped_images.extend(
            await imdb_scraper.extract_posters_from_title_page(imdb_id)
        )

    # Wide sources via Google/Bing and other CDNs
    scraped_images.extend(await image_scraper.scrape_fanart(title))
    scraped_images.extend(await image_scraper.scrape_theposterdb(title))
    scraped_images.extend(await image_scraper.scrape_tvdb(title))
    scraped_images.extend(await image_scraper.scrape_anidb(title))
    scraped_images.extend(await image_scraper.scrape_mal(title))
    scraped_images.extend(await image_scraper.scrape_alphacoders(title))
    scraped_images.extend(await image_scraper.scrape_wallhaven(title))
    scraped_images.extend(await image_scraper.scrape_cinematerial(title))
    scraped_images.extend(await image_scraper.scrape_movieposterdb(title))
    scraped_images.extend(await image_scraper.scrape_wikimedia(title))
    scraped_images.extend(await image_scraper.scrape_bing_images(title))

    all_images = tmdb_images + scraped_images
    all_images = dedupe_images(all_images)
    all_images = sort_images(all_images)

    detected_type = await detect_content_type(query)
    if media_type == "tv" and detected_type == "Movie/TV":
        detected_type = "TV Show"
    if media_type == "movie" and detected_type == "Movie/TV":
        detected_type = "Movie"

    return {
        "title": title,
        "year": year_val,
        "rating": rating,
        "genres": genres,
        "overview": overview,
        "content_type": detected_type,
        "images": all_images,
    }
