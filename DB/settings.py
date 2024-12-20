from typing import Optional
from dataclasses import dataclass
from DB.db_types import DBType


@dataclass
class VectorDBSettings:
    """Settings for initializing a vector database client."""
    db_type: DBType
    url: Optional[str] = None
    api_key: Optional[str] = None
