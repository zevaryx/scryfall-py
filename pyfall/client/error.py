from typing import TYPE_CHECKING

import httpx

if TYPE_CHECKING:
    from pyfall.client.route import Route

class LibraryException(Exception):
    """Base Exception of pyfall."""

class HTTPException(LibraryException):
    """
    An HTTP request resulted in an exception.
    
    Attributes:
        response httpx.Response: The response of the HTTP request
        details str: The text of the exception, could be None
        status int: The HTTP status code
        route Route: The HTTP route that was used
    """
    
    def __init__(self, response: httpx.Response, route: "Route") -> None:
        self.response: httpx.Response = response
        self.route: "Route" = route
        
        data = response.json()
        
        self.status: int = data.get("status")
        self.code: str = data.get("code")
        self.details: str = data.get("details")
        self.type: str | None = data.get("type", None)
        self.warnings: list[str] | None = data.get("warnings", None)
        
        super().__init__(f"{self.status}|{self.code}: {f'({self.type})' if self.type else ''}{self.details}")
        
    def __str__(self) -> str:
        if not self.warnings:
            return f"HTTPException: {self.status}|{self.code} || {self.details}"
        return f"HTTPException: {self.status}|{self.code}: " + "\n".join(self.warnings)
    
    def __repr__(self) -> str:
        return str(self)

class ScryfallError(HTTPException):
    """An error occurred with Scryfall."""   
    
class BadRequest(HTTPException):
    """A bad request was made."""
    
class Forbidden(HTTPException):
    """You do not have access to this."""
        
class NotFound(HTTPException):
    """This resource could not be found."""