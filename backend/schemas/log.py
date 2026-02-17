from pydantic import BaseModel, ConfigDict
from datetime import datetime

class LogResponse(BaseModel):
    id: int
    timestamp: datetime
    action: str
    item_id: str | None
    message: str | None
    status: str | None

    model_config = ConfigDict(from_attributes=True)