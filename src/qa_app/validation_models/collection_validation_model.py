from typing import Optional

from pydantic import BaseModel


class CreateCollectionRequest(BaseModel):
    collection_name: str
    collection_description: str


class UpdateCollectionRequest(BaseModel):
    collection_name: Optional[str]
    collection_description: Optional[str]
