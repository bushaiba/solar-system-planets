import unittest

from src.models.planet import Planet
from src.services.catalogue import PlanetCatalogue
from src.services.query_parser import QueryEngine


def build_catalogue() -> PlanetCatalogue:
    planets = []

    planets.append(
        Planet(
            name="Earth",
            mass_kg=5.972e24,
            distance_from_sun_km=149600000,
            moons=["Moon"],
        )
    )
    planets.append(
        Planet(
            name="Mars",
            mass_kg=6.417e23,
            distance_from_sun_km=227900000,
            moons=["Phobos", "Deimos"],
        )
    )
    planets.append(
        Planet(
            name="Saturn",
            mass_kg=5.683e26,
            distance_from_sun_km=1433500000,
            moons=["Titan", "Enceladus"],
        )
    )
    planets.append(
        Planet(
            name="Neptune",
            mass_kg=1.024e26,
            distance_from_sun_km=4495100000,
            moons=["Triton"],
        )
    )

    return PlanetCatalogue(planets)


class TestQueryEngine(unittest.TestCase):
    def setUp(self) -> None:
        self.catalogue = build_catalogue()
        self.engine = QueryEngine()

    def test_details_query(self) -> None:
        answer = self.engine.answer("Tell me everything about Saturn", self.catalogue)
        self.assertIn("Name: Saturn", answer)

    def test_mass_query(self) -> None:
        answer = self.engine.answer("How massive is Neptune", self.catalogue)
        self.assertIn("Neptune", answer)
        self.assertIn("mass", answer.lower())

    def test_moon_count_query(self) -> None:
        answer = self.engine.answer("How many moons does Earth have", self.catalogue)
        self.assertIn("Earth", answer)
        self.assertIn("1", answer)

    def test_moon_list_query(self) -> None:
        answer = self.engine.answer("List the moons of Mars", self.catalogue)
        self.assertIn("Mars", answer)
        self.assertIn("Phobos", answer)
        self.assertIn("Deimos", answer)

    def test_membership_query_not_in_list(self) -> None:
        answer = self.engine.answer("Is Pluto in the list of planets", self.catalogue)
        self.assertIn("No", answer)
        self.assertIn("pluto", answer.lower())

    def test_misspelling_suggests(self) -> None:
        answer = self.engine.answer("How massive is saturnn", self.catalogue)
        lowered = answer.lower()
        self.assertTrue(("did you mean" in lowered) or ("saturn" in lowered))
