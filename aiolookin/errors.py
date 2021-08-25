"""Define package exceptions."""


class LookInError(Exception):
    """Define a base exception."""

    pass


class CommandError(LookInError):
    """Define a command-related error."""

    pass


class RequestError(LookInError):
    """Define an error related a bad HTTP request."""

    pass


class SensorError(LookInError):
    """Define a sensor-related error."""

    pass
