from pydantic import BaseModel, EmailStr, field_validator
from typing import Literal

# Schema definitions
VALID_SUBJECTS = Literal[
    "New Project Inquiry",
    "General Question",
    "Collaboration",
    "Other",
]

class ContactRequest(BaseModel):
    name: str
    email: EmailStr
    subject: VALID_SUBJECTS
    message: str

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Name must not be empty.")
        if len(v) > 100:
            raise ValueError("Name must be 100 characters or fewer.")
        return v

    @field_validator("message")
    @classmethod
    def message_not_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Message must not be empty.")
        if len(v) > 5000:
            raise ValueError("Message must be 5000 characters or fewer.")
        return v


class ContactResponse(BaseModel):
    success: bool
    message: str
