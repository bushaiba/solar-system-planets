# External references for patterns used in this project are listed in README.md and docs/REFERENCES.md

import json
import difflib
from pathlib import Path
from typing import List, Dict, Any

from src.models.planet import Planet
from src.utils.errors import DataValidationError, PlanetNotFoundError
from src.utils.text import normalise_name


class PlanetCatalogue:
    def __init__(self, planets: List[Planet]) -> None:
        """
        Create a catalogue of Planet objects indexed by a normalised name.

        This builds an internal dictionary mapping:
        normalise_name(planet.name) -> Planet
        so lookups are fast and case/spacing insensitive.
        """
        self._by_name: Dict[str, Planet] = {normalise_name(planet.name): planet for planet in planets}  # Dict[str, Planet] adding type hint for clarity

        # self._by_name: Dict[str, Planet] = {}
        # for p in planets:
        #     key = normalise_name(p.name)
        #     self._by_name[key] = p

    @classmethod
    def from_json(cls, path: str | Path) -> "PlanetCatalogue":
        """
        Load planet data from a JSON file and return a PlanetCatalogue instance.

        Validates:
        - file exists
        - JSON is valid
        - top-level JSON is a list
        - each list entry is an object (dict)
        - required fields are present and valid for constructing Planet objects

        Raises DataValidationError if the file is missing or the data is invalid.
        """
        path = Path(path)
        if not path.exists():
            raise DataValidationError(f"File not found: {path}")

        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise DataValidationError(f"Invalid JSON in {path}: {exc}") from exc

        if not isinstance(raw, list):
            raise DataValidationError("Planet data must be a list of planet objects")

        planets: List[Planet] = []

        for idx, item in enumerate(raw):
            # enumerate gives the list index (idx) so validation errors can point to the exact bad entry.
            if not isinstance(item, dict):
                raise DataValidationError(f"Planet entry at index {idx} must be a JSON object.")

            try:
                planet = Planet(
                    name=item["name"],
                    mass_kg=item["mass_kg"],
                    distance_from_sun_km=item["distance_from_sun_km"],
                    moons=item.get("moons", []),
                )
            except KeyError as exc:
                raise DataValidationError(
                    f"Missing required planet field {exc} in entry at index {idx}."
                ) from exc
            except DataValidationError as exc:
                raise DataValidationError(
                    f"Invalid data for planet {item.get('name', 'unknown')!r}: {exc}"
                ) from exc

            planets.append(planet)

        return cls(planets)

    def exists(self, name: str) -> bool:
        """
        Check whether a planet exists in the catalogue by name.

        The name is normalised so the check is case/spacing insensitive.
        Returns True if found, otherwise False.
        """
        return normalise_name(name) in self._by_name

    def get(self, name: str) -> Planet:
        """
        Return the Planet object matching the given name.

        The name is normalised so the lookup is case/spacing insensitive.
        Raises PlanetNotFoundError if no matching planet is found.
        """
        key = normalise_name(name)

        if key not in self._by_name:
            raise PlanetNotFoundError(f"Planet not found: {name}")
        return self._by_name[key]

    def all_names(self) -> List[str]:
        """
        Return a sorted list of all planet names in the catalogue.

        The returned names are the original Planet.name values (not normalised).
        """
        return sorted(p.name for p in self._by_name.values())

    def suggest(self, name: str, limit: int = 3) -> List[str]:
        """
        Suggest close planet-name matches for a user-provided name.

        Uses difflib.get_close_matches to find similar normalised keys.
        Returns up to 'limit' suggestions as original planet names.
        """
        key = normalise_name(name)

        keys = list(self._by_name.keys())
        matches = difflib.get_close_matches(key, keys, n=limit, cutoff=0.6)
        # difflib is a Python standard library module for comparing sequences like strings and lists

        suggestions: List[str] = []
        for match in matches:
            suggestions.append(self._by_name[match].name)

        return suggestions
