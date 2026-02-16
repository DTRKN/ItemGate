from pydantic import BaseModel
from datetime import datetime

class LogResponse(BaseModel):
    id: int
    timestamp: datetime
    action: str
    item_id: str | None
    message: str | None
    status: str | None

    class Config:
        from_attributes = True