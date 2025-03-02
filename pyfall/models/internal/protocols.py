import typing
from typing import Protocol, Any, TypeVar

from pyfall.client.route import Route

T_co = TypeVar("T", covariant=True)  # type: ignore


@typing.runtime_checkable
class CanRequest(Protocol[T_co]):
    async def request(
        self,
        route: Route,
        params: dict | None = None,
        **kwargs: dict,
    ) -> dict[str, Any]:
        raise NotImplementedError("Derived classes need to implement this.")
