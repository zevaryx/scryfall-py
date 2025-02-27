from typing import Any, Literal

from pyfall.models.catalogs import Catalog
from pyfall.client.route import Route
from pyfall.models.cards import Card
from pyfall.models.api import APIList
from pyfall.models.rulings import Ruling
from pyfall.models.sets import Set
from pyfall.models.internal.protocols import CanRequest

class SetRequests(CanRequest):
    async def get_all_sets(self) -> APIList:
        """Get all MTG sets."""
        result = await self.request(Route("GET", "/sets"))
        
        result["_client"] = self
        return APIList(**result)
    
    async def get_set_by_id(self, id: str) -> Set:
        """Get MTG set by ID.

        Args:
            id: UUID of set
        """
        result = await self.request(Route("GET", f"/sets/{id}"))
        
        result["_client"] = self
        return Set(**result)
    
    async def get_set_by_code(self, code: str) -> Set:
        """Get MTG set by set code.

        Args:
            code: Set code
        """
        result = await self.request(Route("GET", f"/sets/{code}"))
        
        result["_client"] = self
        return Set(**result)
    
    async def get_set_by_tcgplayer_id(self, id: str) -> Set:
        """Get MTG set by TCGPlayer ID.

        Args:
            id: TCGPlayer ID of set
        """
        result = await self.request(Route("GET", f"/sets/tcgplayer/{id}"))
        
        result["_client"] = self
        return Set(**result)