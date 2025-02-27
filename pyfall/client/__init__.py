from typing import Any, Literal

import httpx

from pyfall.const import __version__
from pyfall.models import *
from pyfall.utils import UUID_CHECK

import asyncio
import logging
import time
from typing import Any

from httpx import AsyncClient

from pyfall.const import __version__, get_logger
from pyfall.client.error import *
from pyfall.client.http.http_requests.card import CardRequests
from pyfall.client.http.http_requests.set import SetRequests
from pyfall.client.route import Route

class GlobalLock:
    def __init__(self) -> None:
        self._lock = asyncio.Lock()
        self.max_requests = 10
        self._calls = self.max_requests
        self._reset_time = 0

    @property
    def calls_remaining(self) -> int:
        """Returns the amount of calls remaining."""
        return self.max_requests - self._calls

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
            "Accept": "application/json"
        }
        self.__client: AsyncClient = None
        self.global_lock: GlobalLock = GlobalLock()
        self._max_attempts: int = 3
        
        self.logger = logger
        if self.logger is None:
            self.logger = get_logger()
            
    async def request(self, route: Route, params: dict | None = None, **kwargs: dict) -> dict[str, Any]:
        """Make a request to the Scryfall API.

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
            if self.__client is None:
                self.__client = AsyncClient()
            
            await self.global_lock.wait()
            
            response = await self.__client.request(route.method, route.url, **kwargs)
            
            if response.status_code == 429:
                self.logger.warning("Too many requests, waiting 5 seconds")
                self.global_lock.set_reset_time(5)
                continue
            
            if response.status_code >= 500:
                self.logger.warning(f"{route.resolved_endpoint} Received {response.status_code}... retrying in {1 + attempt * 2} seconds")
                await asyncio.sleep(1 + attempt * 2)
                continue
            
            result = response.json()
            
            if not 300 > response.status_code >= 200:
                await self._raise_exception(response, route, result)
            
            
            
            return result

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

# class Pyfall:
#     """Scryfall API client."""
#     def __init__(self):
#         self._headers = {
#             "Content-Type": "application/json", 
#             "UserAgent": f"pyfall/{__version__}", 
#             "Accept": "application/json"
#         }
#         self.__httpx: httpx.AsyncClient = None
        
#     async def request(self, endpoint: str, method: str = "GET", **kwargs) -> dict[str, Any]:
#         """Make a request to the API.
        
#         Args:
#             endpoint: Endpoint to request from
            
#         Returns:
#             Raw API result
#         """
#         if not self.__httpx:
#             self.__httpx = httpx.AsyncClient(headers=self._headers, base_url="https://api.scryfall.com")
            
#         args = {k: v for k, v in kwargs if v is not None}
        
#         if method not in ("POST", "PATCH", "PUT"):
#             response: httpx.Response = await self.__httpx.request(method=method, url=endpoint, params=args)
#         else:
#             response: httpx.Response = await self.__httpx.request(method=method, url=endpoint, data=args)
#         if response.status_code >= 500:
#             response.raise_for_status()
#         data = response.json()
        # return data
        
    # async def get_card_by_id(self, id: str) -> Card:
    #     """Get a card by ID.
        
    #     Args:
    #         id: UUID of card  
    #     """
    #     if not UUID_CHECK.match(id):
    #         raise ValueError("'id' must be a UUID")
    #     data = await self.request(f"cards/{id}")
    #     if data["object"] == "error":
    #         return APIError.model_validate(data)
    #     data["_client"] = self
    #     return Card(**data)