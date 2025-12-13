from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from src.utils.errors import DataValidationError


@dataclass(frozen=True, slots=True)  # Using slots for memory efficiency and frozen for immutability. Also @dataclass auto-generates __init__, __repr__, and __eq__ methods.
class Planet:
    """
    Represents a planet in the catalogue with core astronomical attributes.

    Fields:
    - name: planet name (must be a non-empty string)
    - mass_kg: mass in kilograms (must be a positive number)
    - distance_from_sun_km: distance from the Sun in kilometres (must be a positive number)
    - moons: list of moon names (each must be a non-empty string)
    """
    name: str
    mass_kg: float  # Mass in kilograms
    distance_from_sun_km: float  # Distance from the sun in kilometers
    moons: List[str]

    def __post_init__(self) -> None:
        """
        Validate dataclass fields immediately after object creation.

        This runs automatically after the dataclass-generated __init__.
        Raises DataValidationError if any field is missing or invalid.
        """
        if not isinstance(self.name, str) or not self.name.strip():
            raise DataValidationError("Planet name must be a non-empty string")

        if not isinstance(self.mass_kg, (int, float)) or self.mass_kg <= 0:
            raise DataValidationError(f"Mass must be a positive number. Got: {self.mass_kg}")

        if not isinstance(self.distance_from_sun_km, (int, float)) or self.distance_from_sun_km <= 0:
            raise DataValidationError(
                f"Distance from sun must be a positive number. Got: {self.distance_from_sun_km}"
            )

        if not isinstance(self.moons, list):
            raise DataValidationError("Moons must be a list of strings")

        for moon in self.moons:
            if not isinstance(moon, str) or not moon.strip():
                raise DataValidationError("Each moon name must be a non-empty string")

    def moon_count(self) -> int:
        """
        Return the number of moons orbiting the planet.
        """
        return len(self.moons)
