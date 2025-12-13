from src.services.catalogue import PlanetCatalogue
from src.utils.errors import PlanetError


def main() -> None:
    try:
        catalogue = PlanetCatalogue.from_json("data/planets.json")
        print("Loaded planets:", ", ".join(catalogue.all_names()))

        saturn = catalogue.get("saturn")
        print(f"Saturn moons: {saturn.moon_count()}")

    except PlanetError as exc:
        print(f"Error: {exc}")


if __name__ == "__main__":
    main()
