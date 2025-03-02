from typing import Any

from pyfall.const import __version__

import asyncio
import logging
import time

from httpx import AsyncClient

from pyfall.const import get_logger
from pyfall.client.error import LibraryException, HTTPException, ScryfallError, Forbidden, NotFound
from pyfall.client.http.http_requests.card import CardRequests
from pyfall.client.http.http_requests.set import SetRequests
from pyfall.client.route import Route


class GlobalLock:
    def __init__(self) -> None:
        self._lock = asyncio.Lock()
        self.max_requests = 10
        self._calls = self.max_requests
        self._reset_time = 0

    def reset_calls(self) -> None:
        """Resets the calls to the max amount."""
        self._calls = self.max_requests
        self._reset_time = time.perf_counter() + 1

    def set_reset_time(self, delta: float) -> None:
        """
        Sets the reset time to the current time + delta.

        To be called if a 429 is received.

        Args:
            delta: The time to wait before resetting the calls.

        """
        self._reset_time = time.perf_counter() + delta
        self._calls = 0

    async def wait(self) -> None:
        """Throttles calls to prevent hitting the global rate limit."""
        async with self._lock:
            if self._reset_time <= time.perf_counter():
                self.reset_calls()
            elif self._calls <= 0:
                await asyncio.sleep(self._reset_time - time.perf_counter())
                self.reset_calls()
        self._calls -= 1


class Pyfall(CardRequests, SetRequests):
    def __init__(self, logger: logging.Logger | None = None):
        self.__headers = {
            "Content-Type": "application/json",
            "UserAgent": f"pyfall/{__version__}",
            "Accept": "application/json",
        }
        self.__client: AsyncClient = None  # type: ignore
        self.global_lock: GlobalLock = GlobalLock()
        self._max_attempts: int = 3

        self.logger: logging.Logger = logger  # type: ignore
        if self.logger is None:
            self.logger = get_logger()

    async def request(self, route: Route, params: dict | None = None, **kwargs: dict) -> dict[str, Any]:
        """
        Make a request to the Scryfall API.

        Args:
            route: Route to take
            params: Query string parameters. Defaults to None.

        Returns:
            dict[str, Any]: Raw result

        """
        if params is not None:
            kwargs["params"] = params
        if not self.__client:
            self.__client = AsyncClient(headers=self.__headers)
        for attempt in range(self._max_attempts):
            await self.global_lock.wait()

            response = await self.__client.request(route.method, route.url, **kwargs)  # type: ignore

            if response.status_code == 429:
                self.logger.warning("Too many requests, waiting 5 seconds")
                self.global_lock.set_reset_time(5)
                continue

            if response.status_code >= 500:
                self.logger.warning(
                    f"{route.resolved_endpoint} Received {response.status_code}... retrying in {1 + attempt * 2} seconds"
                )
                await asyncio.sleep(1 + attempt * 2)
                continue

            result = response.json()

            if not 300 > response.status_code >= 200:
                await self._raise_exception(response, route, result)

            return result

        raise LibraryException(f"Failed to get endpoint {route.endpoint}")

    async def _raise_exception(self, response, route, result) -> None:
        self.logger.error(f"{route.method}::{route.url}: {response.status_code}")

        if response.status_code == 403:
            raise Forbidden(response, route)
        if response.status_code == 404:
            raise NotFound(response, route)
        if response.status_code >= 500:
            raise ScryfallError(response, route)

        raise HTTPException(response, route)

    async def close(self) -> None:
        """Close the session."""
        if self.__client is not None and not self.__client.is_closed:
            await self.__client.aclose()
