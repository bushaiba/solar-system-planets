import difflib
from enum import Enum
from typing import Optional

from src.services.catalogue import PlanetCatalogue
from src.services.formatter import (
    format_planet_details,
    format_planet_distance,
    format_planet_mass,
    format_planet_moon_count,
    format_planet_moon_list,
    format_membership_result,
)
from src.utils.text import normalise_name


class Intent(str, Enum):
    """
    Represents the supported question types (intents) the QueryEngine can recognise.

    Each value is a simple label used to route the question to the correct answer logic.
    """
    DETAILS = "details"
    MASS = "mass"
    DISTANCE = "distance"
    MOON_COUNT = "moon_count"
    MOON_LIST = "moon_list"
    MEMBERSHIP = "membership"
    UNKNOWN = "unknown"


class QueryEngine:
    """
    Interprets a user's question, detects what they are asking, finds the planet (if any),
    and returns a formatted answer string.
    """

    def answer(self, question: str, catalogue: PlanetCatalogue) -> str:
        """
        Produce an answer to a user question using the provided PlanetCatalogue.

        Steps:
        - normalise and validate the input question
        - detect the intent (mass, distance, moons, etc.)
        - extract a planet name from the question (if present)
        - return the correctly formatted response or a helpful fallback message
        """
        cleaned = normalise_name(question)
        if cleaned == "":
            return "Please enter a question."

        intent = self._detect_intent(cleaned)

        planet_name = self._extract_planet_name(cleaned, catalogue)

        if intent == Intent.MEMBERSHIP:
            return self._answer_membership(cleaned, planet_name, catalogue)

        if planet_name is None:
            suggestions = self._suggest_from_text(cleaned, catalogue)
            if suggestions:
                return (
                    "Planet not found. Did you mean: "
                    + ", ".join(suggestions)
                    + "?"
                )
            return self._unknown_planet_message(catalogue)

        planet = catalogue.get(planet_name)

        if intent == Intent.DETAILS:
            return format_planet_details(planet)
        if intent == Intent.MASS:
            return format_planet_mass(planet)
        if intent == Intent.DISTANCE:
            return format_planet_distance(planet)
        if intent == Intent.MOON_COUNT:
            return format_planet_moon_count(planet)
        if intent == Intent.MOON_LIST:
            return format_planet_moon_list(planet)

        return self._unknown_question_message()

    def _detect_intent(self, cleaned: str) -> Intent:
        """
        Detect what the user is asking for based on keyword rules.

        Returns an Intent enum value such as:
        - MOON_COUNT if asking "how many moons"
        - MASS if asking about mass/weight
        - DISTANCE if asking distance from the sun
        - DETAILS for broad requests like "tell me everything"
        - MEMBERSHIP for "is X a planet / in the list"
        - UNKNOWN if no rules match
        """
        has_moon = "moon" in cleaned or "moons" in cleaned

        if ("how many" in cleaned or "number of" in cleaned) and has_moon:
            return Intent.MOON_COUNT

        if has_moon and ("list" in cleaned or "what are" in cleaned or "which" in cleaned or "name" in cleaned):
            return Intent.MOON_LIST

        if "mass" in cleaned or "massive" in cleaned or "weigh" in cleaned or "weight" in cleaned:
            return Intent.MASS

        if "distance" in cleaned or "far" in cleaned or "from the sun" in cleaned:
            return Intent.DISTANCE

        if "everything" in cleaned or "tell me" in cleaned or "all about" in cleaned or "details" in cleaned:
            return Intent.DETAILS

        if "is " in cleaned and ("in the list" in cleaned or "a planet" in cleaned or "planet" in cleaned):
            return Intent.MEMBERSHIP

        return Intent.UNKNOWN

    def _extract_planet_name(self, cleaned: str, catalogue: PlanetCatalogue) -> Optional[str]:
        """
        Try to find a planet name inside the cleaned question text.

        This checks for whole-word matches by padding the string with spaces, so
        'mars' matches '... mars ...' but avoids partial matches inside other words.

        Returns the original planet name (as stored in the catalogue) if found,
        otherwise returns None.
        """
        padded = " " + cleaned + " "
        names = catalogue.all_names()

        for name in names:
            key = normalise_name(name)
            needle = " " + key + " "
            if needle in padded:
                return name

        return None

    def _answer_membership(self, cleaned: str, planet_name: Optional[str], catalogue: PlanetCatalogue) -> str:
        """
        Answer questions like 'Is Pluto a planet?' or 'Is Mars in the list of planets?'.

        If a planet name is already extracted from the question, it returns a positive membership response.
        Otherwise it tries to guess a candidate name from the text, checks the catalogue,
        and returns a formatted yes/no with optional suggestions for close matches.
        """
        if planet_name is not None:
            return format_membership_result(planet_name, True)

        candidate = self._extract_membership_candidate(cleaned)
        if candidate is None:
            return "Please provide a name to check."

        if catalogue.exists(candidate):
            planet = catalogue.get(candidate)
            return format_membership_result(planet.name, True)

        suggestions = catalogue.suggest(candidate)
        if suggestions:
            return format_membership_result(candidate, False) + " Did you mean: " + ", ".join(suggestions) + "?"

        return format_membership_result(candidate, False)

    def _extract_membership_candidate(self, cleaned: str) -> Optional[str]:
        """
        Extract a likely planet name candidate from a membership question.

        This uses a simple heuristic: take the last alphabetic word in the question.
        Returns that word, or None if no suitable token is found.
        """
        tokens = cleaned.split(" ")
        last_word = None

        for token in tokens:
            if token.isalpha():
                last_word = token

        return last_word

    def _suggest_from_text(self, cleaned: str, catalogue: PlanetCatalogue) -> list[str]:
        """
        Suggest planet names based on a likely token inside the user's question.

        Heuristic: choose the last alphabetic word as the best token, then ask the catalogue
        for close matches (e.g., to handle typos like 'marss').
        Returns a list of suggested planet names (may be empty).
        """
        tokens = cleaned.split(" ")
        best_token = None

        for token in tokens:
            if token.isalpha():
                best_token = token

        if best_token is None:
            return []

        return catalogue.suggest(best_token)

    def _unknown_planet_message(self, catalogue: PlanetCatalogue) -> str:
        """
        Build a helpful message when no planet name could be identified or matched.

        Includes the list of valid planet names from the catalogue to guide the user.
        """
        return "Planet not found. Try one of: " + ", ".join(catalogue.all_names())

    def _unknown_question_message(self) -> str:
        """
        Return a fallback message when the question intent cannot be understood.

        Provides example questions to show the user what the system can answer.
        """
        return (
            "I did not understand that question.\n"
            "Try examples like:\n"
            "- Tell me everything about Saturn\n"
            "- How massive is Neptune\n"
            "- How many moons does Earth have\n"
            "- Is Pluto in the list of planets"
        )
