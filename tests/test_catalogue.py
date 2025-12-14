import json
import tempfile
import unittest
from pathlib import Path

from src.models.planet import Planet
from src.services.catalogue import PlanetCatalogue
from src.utils.errors import DataValidationError


class TestPlanetCatalogue(unittest.TestCase):
    def test_from_json_loads_valid_file(self) -> None:
        data = [
            {
                "name": "Earth",
                "mass_kg": 5.972e24,
                "distance_from_sun_km": 149600000,
                "moons": ["Moon"],
            },
            {
                "name": "Saturn",
                "mass_kg": 5.683e26,
                "distance_from_sun_km": 1433500000,
                "moons": ["Titan"],
            },
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "planets.json"
            path.write_text(json.dumps(data), encoding="utf-8")

            catalogue = PlanetCatalogue.from_json(path)
            self.assertTrue(catalogue.exists("earth"))
            self.assertTrue(catalogue.exists("SATURN"))
            self.assertEqual(len(catalogue.all_names()), 2)

    def test_from_json_missing_required_field_raises(self) -> None:
        data = [
            {
                "name": "Earth",
                "distance_from_sun_km": 149600000,
                "moons": ["Moon"],
            }
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "planets.json"
            path.write_text(json.dumps(data), encoding="utf-8")

            with self.assertRaises(DataValidationError):
                PlanetCatalogue.from_json(path)

    def test_suggest_returns_close_match(self) -> None:
        planets = []
        planets.append(
            Planet(
                name="Saturn",
                mass_kg=5.683e26,
                distance_from_sun_km=1433500000,
                moons=["Titan"],
            )
        )
        planets.append(
            Planet(
                name="Earth",
                mass_kg=5.972e24,
                distance_from_sun_km=149600000,
                moons=["Moon"],
            )
        )

        catalogue = PlanetCatalogue(planets)
        suggestions = catalogue.suggest("saturnn")

        self.assertTrue(len(suggestions) >= 1)
        self.assertEqual(suggestions[0], "Saturn")
