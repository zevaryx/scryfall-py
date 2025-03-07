from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, HttpUrl


class BulkData(BaseModel):
    """Bulk data model"""

    id: UUID
    """UUID of the bulk data"""

    uri: HttpUrl
    """URI of the bulk data endpoint"""

    type: str
    """The type of data in the download"""

    name: str
    """The name of the download"""

    description: str
    """A description of the download"""

    download_uri: HttpUrl
    """The download URL for the bulk data"""

    updated_at: datetime
    """When this bulk data was last updated"""

    size: int
    """The size of the data in bytes"""

    content_type: str
    """The content type"""

    content_encoding: str
    """The MIME encoding"""
