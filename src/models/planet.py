from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from src.utils.errors import DataValidationError


@dataclass(frozen=True, slots=True) # Using slots for memory efficiency and frozen for immutability. Also @dataclass auto-generates __init__, __repr__, and __eq__ methods.
class Planet:
    name: str
    mass_kg: float  # Mass in kilograms
    distance_from_sun_km: float  # Distance from the sun in kilometers
    moons: List[str]

    def __post_init__(self): # Post-construction validation for dataclass fields.
        if not isinstance(self.name, str) or not self.name.strip():
            raise DataValidationError("Planet name must be a non-empty string")
        
        if not isinstance(self.mass_kg, (int, float)) or self.mass_kg <= 0:
            raise DataValidationError("Mass must be a positive number. Got: {self.mass_kg}")
        
        if not isinstance(self.distance_from_sun_km, (int, float)) or self.distance_from_sun_km <= 0:
            raise DataValidationError("Distance from sun must be a positive number. Got: {self.distance_from_sun_km}")
        
        if not isinstance(self.moons, List):
            raise DataValidationError("Moons must be a list of strings")
        
        for moon in self.moons:
            if not isinstance(moon, str) or not moon.strip():
                raise DataValidationError("Each moon name must be a non-empty string")
            
    def moon_count(self) -> int:
        """Returns the number of moons orbiting the planet."""
        return len(self.moons)
    
    