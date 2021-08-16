"""Define package exceptions."""


class LookInError(Exception):
    """Define a base exception."""

    pass


class RequestError(LookInError):
    """Define an error related a bad HTTP request."""

    pass
