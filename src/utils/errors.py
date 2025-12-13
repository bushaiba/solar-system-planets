
class PlanetError(Exception):
    """Base error for the planets app"""


class DataValidationError(PlanetError):
    """Raised when loaded planet data is invalid"""


class PlanetNotFoundError(PlanetError):
    """Raised when loaded planet data is invalid"""

