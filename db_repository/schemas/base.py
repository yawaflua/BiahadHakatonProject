from pydantic import BaseModel
from typing import List, Optional


class BaseSchema(BaseModel):
    id: Optional[int] = None
