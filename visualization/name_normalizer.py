from __future__ import annotations

import re
import unicodedata


SPECIAL_CASES = {
    "tp ho chi minh": "ho chi minh",
    "tp. ho chi minh": "ho chi minh",
    "thanh pho ho chi minh": "ho chi minh",
    "ba ria - vung tau": "ba ria vung tau",
    "ba ria vung tau": "ba ria vung tau",
    "thua thien hue": "thua thien hue",
    "hue": "thua thien hue",
}


def strip_accents(text: str) -> str:
    normalized = unicodedata.normalize("NFD", text)
    return "".join(character for character in normalized if unicodedata.category(character) != "Mn")


def slugify_province_name(name: str) -> str:
    lowered = strip_accents(name).lower().strip()
    lowered = (
        lowered
        .replace("đ", "d")
        .replace("ä‘", "d")
        .replace("ð", "d")
    )
    lowered = re.sub(r"[^\w\s.-]", " ", lowered)
    lowered = re.sub(r"\s+", " ", lowered).strip()
    return lowered


def canonical_province_name(name: str) -> str:
    slug = slugify_province_name(name)
    return SPECIAL_CASES.get(slug, slug)
