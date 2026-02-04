from typing import Any, Dict, List, Optional
import hashlib
import re


def normalize_query(text: str) -> str:
    return re.sub(r"s+", " ", text.strip()).lower()


def extract_year_from_query(text: str) -> tuple[str, Optional[int]]:
    pattern = r"(.*?)(?:s+(d{4}))?$"
    m = re.match(pattern, text.strip())
    if not m:
        return text.strip(), None
    title = m.group(1).strip()
    year = m.group(2)
    return (title, int(year)) if year else (title, None)


def hash_url(url: str) -> str:
    return hashlib.sha256(url.encode("utf-8")).hexdigest()


def dedupe_images(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    seen = set()
    out: List[Dict[str, Any]] = []
    for item in items:
        url = item.get("url")
        if not url:
            continue
        h = hash_url(url)
        if h in seen:
            continue
        seen.add(h)
        out.append(item)
    return out


def sort_images(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    def score(x: Dict[str, Any]) -> int:
        w = x.get("width") or 0
        h = x.get("height") or 0
        res = w * h
        popularity = x.get("popularity") or 0
        clean_crop = 1 if x.get("clean") else 0
        return res * 3 + popularity * 5 + clean_crop * 50

    return sorted(items, key=score, reverse=True)


def build_caption_box(
    title: str,
    year: Optional[int],
    rating: Optional[float],
    content_type: str,
    overview: str,
    genres: List[str],
    audio_info: Optional[str] = None,
) -> str:
    line = "─" * 38
    header = f"🎬 {title}"
    if year:
        header += f" ({year})"
    type_line = f"🎭 Type : {content_type}"
    rating_line = f"⭐ Rating : {rating:.1f}/10" if rating is not None else "⭐ Rating : N/A"
    quality_line = "📁 Quality : 480p | 720p | 1080p"
    audio_line = f"🔈 Audio : {audio_info}" if audio_info else "🔈 Audio : N/A"
    genres_line = f"🎯 Genres : {', '.join(genres) if genres else 'N/A'}"
    trimmed_overview = overview.strip() if overview else "No synopsis available."
    if len(trimmed_overview) > 900:
        trimmed_overview = trimmed_overview[:897] + "..."
    synopsis = "🧾 Synopsis :
" + trimmed_overview
    return (
        f"{line}
"
        f"{header}
"
        f"{line}
"
        f"{type_line}
"
        f"{rating_line}
"
        f"{quality_line}
"
        f"{audio_line}
"
        f"{genres_line}
"
        f"{line}
"
        f"{synopsis}
"
        f"{line}"
    )

def safe_get(d: Dict[str, Any], *keys, default=None):
    cur = d
    for k in keys:
        if not isinstance(cur, dict) or k not in cur:
            return default
        cur = cur[k]
    return cur
