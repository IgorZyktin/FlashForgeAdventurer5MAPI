"""Custom exceptions."""


class GeneralException(Exception):
    """Base class for exceptions."""


class UnexpectedResponse(GeneralException):
    """Printer returned something we could not parse."""
