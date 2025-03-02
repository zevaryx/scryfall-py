from typing import Any, ClassVar
from urllib.parse import quote as _uriquote

PAYLOAD_TYPE = dict[str, int | str | bool | list | None]


class Route:
    BASE: ClassVar[str] = "https://api.scryfall.com"
    path: str
    params: dict[str, str | int | bool]

    def __init__(self, method: str, path: str, **params: Any) -> None:
        self.path: str = path
        self.method: str = method
        self.params = params

    def __repr__(self) -> str:
        return f"<Route {self.endpoint}>"

    def __str__(self) -> str:
        return self.endpoint

    @property
    def resolved_path(self) -> str:
        """The endpoint for this route, with all parameters resolved"""
        return self.path.format_map({k: _uriquote(v) if isinstance(v, str) else v for k, v in self.params.items()})

    @property
    def endpoint(self) -> str:
        """The endpoint for this route"""
        return f"{self.method} {self.path}"

    @property
    def resolved_endpoint(self) -> str:
        """The endpoint for this route, with all major parameters resolved"""
        return f"{self.method} {self.path}"

    @property
    def url(self) -> str:
        """The full url for this route"""
        return f"{self.BASE}{self.resolved_path}"
