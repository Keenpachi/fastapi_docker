from pydantic import BaseModel, Field
from datetime import date


class ClientSchema(BaseModel):
    id: int
    name: str
    card_id: str = Field(min_length=6, max_length=6)

    class Config:
        orm_mode = True


class BookSchema(BaseModel):
    id: int
    serial_number: str = Field(min_length=6, max_length=6)
    title: str
    author: str
    available: bool
    rental_date: date
    client_id: int | None = None

    class Config:
        orm_mode = True
