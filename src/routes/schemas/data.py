from pydantic import BaseModel, validator
from typing import Optional

class ProcessRequest(BaseModel):
    file_id: str
    chunk_size: Optional[int] = 100
    overlap_size: Optional[int] = 20
    do_reset: Optional[bool] = False

    @validator('chunk_size')
    def validate_chunk_size(cls, v):
        if v < 100 or v > 1000:
            raise ValueError('chunk_size must be between 100 and 1000')
        return v

    @validator('overlap_size')
    def validate_overlap_size(cls, v):
        if v < 20:
            raise ValueError('overlap_size must be at least 20')
        return v
