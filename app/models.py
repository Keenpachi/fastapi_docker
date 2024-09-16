from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .database import Base


class Client(Base):
    __tablename__ = 'client'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    card_id = Column(String(6), index=True)


class Book(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, index=True)
    serial_number = Column(String(6), index=True)
    title = Column(String(255), index=True)
    author = Column(String(255), index=True)
    available = Column(Boolean, index=True)
    rental_date = Column(String(60), index=True)
    client_id = Column(Integer, ForeignKey("client.id"))

    client = relationship("Client")

