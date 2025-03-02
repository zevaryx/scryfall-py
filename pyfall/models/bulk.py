from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, HttpUrl


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
