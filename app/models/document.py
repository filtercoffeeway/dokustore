from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Document():
    id: int
    document_name: str
    document_type_id: int
    user_id: int
    status: str
    file_id: Optional[int] = None
    file_path: Optional[str] = None
    file_type: Optional[str] = None
    file_size: Optional[float] = None
    due_date: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

@dataclass
class DocumentSummary():
    total_documents: int
    total_file_size: float
    documents_past_due: int