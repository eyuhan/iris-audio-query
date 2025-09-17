from pydantic import BaseModel
from typing import Any


class AudioUploadRequest(BaseModel):
    file: Any


class AudioUploadResponse(BaseModel):
    pass


class AudioQueryRequest(BaseModel):
    query: str


class AudioQueryResponse(BaseModel):
    pass
