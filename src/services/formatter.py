from src.models.planet import Planet


def format_planet_details(planet: Planet) -> str:
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
    return f"{planet.name} mass (kg): {planet.mass_kg:.3e}"


def format_planet_distance(planet: Planet) -> str:
    return f"{planet.name} distance from Sun (km): {planet.distance_from_sun_km:,.0f}"


def format_planet_moon_count(planet: Planet) -> str:
    return f"{planet.name} has {planet.moon_count()} moon(s)."
