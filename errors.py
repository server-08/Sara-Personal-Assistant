"""SARA — Custom Exceptions"""


class SARAError(Exception):
    """Base exception for all SARA errors."""


class MissingAPIKeyError(SARAError):
    """Raised when API_KEY is not set in .env."""
