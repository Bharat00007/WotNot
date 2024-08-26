from pydantic import BaseModel

# Pydantic model
class ContactCreate(BaseModel):
    name: str
    email: str
    phone: str
    tags: list[str] = []

class ContactRead(ContactCreate):
    id: int
    