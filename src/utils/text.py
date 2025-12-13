import re


def normalise_name(name: str) -> str:
    """
    Normalise a planet name for consistent formatting/matching.
    e.g. "saTUrN" -> "saturn"
    """

    name = name.strip().lower()
    name = re.sub(r"\s+", " ", name)  # Replace multiple spaces with a single space
    return name