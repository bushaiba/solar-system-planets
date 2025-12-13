from src.services.catalogue import PlanetCatalogue
from src.services.formatter import (
    format_planet_details,
    format_planet_distance,
    format_planet_mass,
    format_planet_moon_count,
)
from src.services.query_parser import QueryEngine
from src.utils.errors import PlanetError, PlanetNotFoundError


def prompt(text: str) -> str:
    """
    Prompt the user for input, strip leading/trailing whitespace, and return the result.

    Also prints a blank line after input for nicer console spacing.
    """
    value = input(text).strip()
    print()
    return value


def prompt_non_empty(text: str) -> str:
    """
    Prompt the user until they enter a non-empty value.

    Returns the stripped input string once it is not empty.
    """
    while True:
        value = input(text).strip()
        if value != "":
            print()
            return value
        print("Please enter a value.")


def normalise_menu_choice(raw: str) -> str:
    """
    Convert a raw menu input into a normalised menu code.

    Accepts:
    - digits (e.g., "1", "2") and returns them unchanged
    - common keywords (e.g., "list", "exit", "ask") and maps them to menu numbers
    Returns:
    - "" if the input is empty
    - "invalid" if it does not match any supported option
    """
    value = raw.strip().lower()

    if value == "":
        return ""

    if value.isdigit():
        return value

    if value in ["exit", "quit", "q", "x"]:
        return "0"

    if value in ["list", "list planets", "planets", "show planets"]:
        return "1"

    if value in ["details", "planet details", "about", "everything"]:
        return "2"

    if value in ["mass", "planet mass", "how massive"]:
        return "3"

    if value in ["distance", "dist", "how far", "from the sun"]:
        return "4"

    if value in ["moons", "moon count", "how many moons"]:
        return "5"

    if value in ["check", "exists", "is it a planet", "in the list"]:
        return "6"

    if value in ["ask", "question", "query", "free text"]:
        return "7"

    return "invalid"


def show_menu() -> None:
    """
    Print the main menu options to the console.
    """
    print("\nSolar System Planets")
    print("1) List planets")
    print("2) Planet details")
    print("3) Planet mass")
    print("4) Planet distance from Sun")
    print("5) Moon count")
    print("6) Check if a name is a planet in the list")
    print("7) Ask a question")
    print("0) Exit")


def main() -> None:
    """
    Run the command-line menu program.

    Loads the planet data from JSON, then repeatedly:
    - shows the menu
    - reads and normalises a user choice
    - performs the requested action (including free-text questions via QueryEngine)
    Handles common errors and keeps running until the user exits.
    """
    try:
        catalogue = PlanetCatalogue.from_json("data/planets.json")
    except PlanetError as exc:
        print(f"Error loading data: {exc}")
        return

    engine = QueryEngine()

    while True:
        show_menu()
        print()
        raw_choice = prompt("Choose an option (number or words): ")
        choice = normalise_menu_choice(raw_choice)

        if choice == "":
            continue

        if choice == "0":
            print("Goodbye.")
            print()
            break

        if choice == "invalid":
            print("Invalid option. Choose a number from the menu, or type a keyword like 'list'.")
            continue

        try:
            if choice == "1":
                print("Planets:", ", ".join(catalogue.all_names()))

            elif choice == "2":
                name = prompt_non_empty("Enter planet name: ")
                planet = catalogue.get(name)
                print(format_planet_details(planet))

            elif choice == "3":
                name = prompt_non_empty("Enter planet name: ")
                planet = catalogue.get(name)
                print(format_planet_mass(planet))

            elif choice == "4":
                name = prompt_non_empty("Enter planet name: ")
                planet = catalogue.get(name)
                print(format_planet_distance(planet))

            elif choice == "5":
                name = prompt_non_empty("Enter planet name: ")
                planet = catalogue.get(name)
                print(format_planet_moon_count(planet))

            elif choice == "6":
                name = prompt_non_empty("Enter name to check: ")
                if catalogue.exists(name):
                    print(f"Yes, {name.strip()} is in the planet list.")
                else:
                    print(f"No, {name.strip()} is not in the planet list.")

            elif choice == "7":
                question = prompt_non_empty("Ask your question: ")
                answer = engine.answer(question, catalogue)
                print(answer)

            else:
                print("Invalid option. Choose a number from the menu, or type a keyword like 'list'.")

        except PlanetNotFoundError as exc:
            print(f"{exc}. Try one of: {', '.join(catalogue.all_names())}")
        except PlanetError as exc:
            print(f"Error: {exc}")


if __name__ == "__main__":
    main()
