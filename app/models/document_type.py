from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime

@dataclass
class DocumentType():
    id: int
    document_type: str
    user_id: int
    status: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None