import json
from pathlib import Path
from typing import List, Dict, Any

from src.models.planet import Planet
from src.utils.errors import DataValidationError, PlanetNotFoundError
from src.utils.text import normalise_name


class PlanetCatalogue:
    def __init__(self, planets: List[Planet]) -> None:
        self._by_name: Dict[str, Planet] = {normalise_name(planet.name): planet for planet in planets} # Dict[str, Planet] adding type hint for clarity
        
        # self._by_name: Dict[str, Planet] = {}

        # for p in planets:
        #     key = normalise_name(p.name)
        #     self._by_name[key] = p

    @classmethod
    def from_json(cls, path: str | Path) -> "PlanetCatalogue":
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
        return normalise_name(name) in self._by_name
    
    def get(self, name: str) -> Planet:
        key = normalise_name(name)
        
        if key not in self._by_name:
            raise PlanetNotFoundError(f"Planet not found: {name}")
        return self._by_name[key]
    
    def all_names(self) -> List[str]:
        return sorted(p.name for p in self._by_name.values())