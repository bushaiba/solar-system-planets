import unittest

from src.models.planet import Planet
from src.utils.errors import DataValidationError


class TestPlanetModel(unittest.TestCase):
    def test_valid_planet_creates(self) -> None:
        planet = Planet(
            name="Earth",
            mass_kg=5.972e24,
            distance_from_sun_km=149600000,
            moons=["Moon"],
        )
        self.assertEqual(planet.name, "Earth")
        self.assertEqual(planet.moon_count(), 1)

    def test_invalid_name_raises(self) -> None:
        with self.assertRaises(DataValidationError):
            Planet(
                name="",
                mass_kg=1.0,
                distance_from_sun_km=1.0,
                moons=[],
            )

    def test_invalid_mass_raises(self) -> None:
        with self.assertRaises(DataValidationError):
            Planet(
                name="Earth",
                mass_kg=0,
                distance_from_sun_km=1.0,
                moons=[],
            )

    def test_invalid_distance_raises(self) -> None:
        with self.assertRaises(DataValidationError):
            Planet(
                name="Earth",
                mass_kg=1.0,
                distance_from_sun_km=-10,
                moons=[],
            )

    def test_invalid_moons_type_raises(self) -> None:
        with self.assertRaises(DataValidationError):
            Planet(
                name="Earth",
                mass_kg=1.0,
                distance_from_sun_km=1.0,
                moons="Moon",  # type: ignore[arg-type]
            )
