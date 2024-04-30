from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime

@dataclass
class User():
    id: int
    first_name: str
    last_name: str
    email: str
    phone: str
    status: str
    verified_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    username: Optional[str] = None
    deactivated_at: Optional[datetime] = None