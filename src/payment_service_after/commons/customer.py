from typing import Optional
from pydantic import BaseModel

from .contanct import ContactInfo


class CustomerData(BaseModel):
    name: str
    contact_info: ContactInfo
    customer_id: Optional[str] = None