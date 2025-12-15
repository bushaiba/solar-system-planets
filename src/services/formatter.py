# External references for patterns used in this project are listed in README.md and docs/REFERENCES.md

from src.models.planet import Planet


def format_planet_details(planet: Planet) -> str:
    """
    Return a multi-line formatted summary of a planet.

    Includes:
    - name
    - mass (scientific notation)
    - distance from the sun (with thousands separators)
    - moon count and moon names (or 'None listed' if there are no moons)
    """
    moons = ", ".join(planet.moons) if planet.moons else "None listed"
    # moons = "None listed"
    # if planet.moons:
    #     moons = ", ".join(planet.moons)

    return (
        f"Name: {planet.name}\n"
        f"Mass (kg): {planet.mass_kg:.3e}\n"
        f"Distance from Sun (km): {planet.distance_from_sun_km:,.0f}\n"
        f"Moons ({planet.moon_count()}): {moons}"
    )


def format_planet_mass(planet: Planet) -> str:
    """
    Return a one-line formatted string showing the planet's mass in kilograms.
    """
    return f"{planet.name} mass (kg): {planet.mass_kg:.3e}"


def format_planet_distance(planet: Planet) -> str:
    """
    Return a one-line formatted string showing the planet's distance from the Sun in kilometres.
    """
    return f"{planet.name} distance from Sun (km): {planet.distance_from_sun_km:,.0f}"


def format_planet_moon_count(planet: Planet) -> str:
    """
    Return a one-line formatted string showing how many moons the planet has.
    """
    return f"{planet.name} has {planet.moon_count()} moon(s)."


def format_planet_moon_list(planet: Planet) -> str:
    """
    Return a formatted string listing the planet's moons.

    If the planet has no moons, returns a message stating that.
    """
    if not planet.moons:
        return f"{planet.name} has no moons."

    moons_text = ", ".join(planet.moons)
    return f"{planet.name} moons: {moons_text}"


def format_membership_result(name: str, is_in_list: bool) -> str:
    """
    Return a formatted yes/no message for whether a name is in the planet list.

    The name is stripped of surrounding whitespace. If the name is empty after stripping,
    it uses a generic label ('That name') to keep the message readable.
    """
    cleaned = name.strip()
    if cleaned == "":
        cleaned = "That name"

    if is_in_list:
        return f"Yes, {cleaned} is in the planet list."

    return f"No, {cleaned} is not in the planet list."
