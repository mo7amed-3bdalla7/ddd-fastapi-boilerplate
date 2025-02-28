from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID


@dataclass
class User:
    username: str
    email: str
    full_name: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    id: Optional[UUID] = None
