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
    password: Optional[str] = None
    login_retries: Optional[int] = None
    auth_token: Optional[str] = None
    auth_expires_at: Optional[datetime] = None
    auth_created_at: Optional[datetime] = None
    verification_token: Optional[str] = None
    verified_at: Optional[datetime] = None
    reset_token: Optional[str] = None
    reset_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deactivated_at: Optional[datetime] = None