from enum import Enum

from sqlmodel import SQLModel, Field

class WorkStatus(Enum):
    WORKING = "working"
    COMPLETED = "completed"
    
class WorkRecord(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    start_time: str
    end_time: str
    status: WorkStatus = Field(default=WorkStatus.WORKING)


