from datetime import datetime

from pydantic import BaseModel, HttpUrl
from pydantic.types import UUID

class BulkData(BaseModel):
    id: UUID
    uri: HttpUrl
    type: str
    name: str
    description: str
    download_uri: HttpUrl
    updated_at: datetime
    size: int
    content_type: str
    content_encoding: str