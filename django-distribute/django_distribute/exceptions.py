"""Defines custom exceptions used by distribute."""


class InvalidBlueprintException(Exception):
    """Exception raised when an imported blueprint is invalid."""

    def __init__(self, message) -> None:
        super().__init__(message)


class InvalidItemException(Exception):
    """Exception raised when importing an invalid item."""

    def __init__(self, item) -> None:
        self.message = "Invalid item imported"
        self.item = item
        super().__init__(self.message)

    def __str__(self) -> str:
        return f"{self.message}: {self.item}"


class ChestIndexException(Exception):
    """Exception raised when the chest slot index is out of bounds."""

    def __init__(self) -> None:
        self.message = "Chest index is out of bounds."
        super().__init__(self.message)
