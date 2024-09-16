from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.sql import Executable
from .models import *
from .schemas import *


def get_client_by_name(db: Session, name: str):
    return db.query(Client).filter(Client.name == name).first()


def create_client(db: Session, client: ClientSchema):
    db_client = Client(name=client.name, card_id=client.card_id)
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client


def get_book_by_serial_number(db: Session, serial_number: str):
    return db.query(Book).filter(Book.serial_number == serial_number).first()


def create_book(db: Session, book: BookSchema):
    db_book = Book(serial_number=book.serial_number, title=book.title, author=book.author, available=book.available, rental_date=book.rental_date)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def del_book(db: Session, serial_number: str):
    db_book = db.query(Book).filter(Book.serial_number == serial_number).first()
    db.delete(db_book)
    db.commit()
    return True


def paginate_books_list(db: Session, page: int, size: int) -> list[Book]:
    statement: Executable = select(Book).offset((page-1)*size).limit(size)
    result: list[Book] = db.execute(statement).scalars().all()
    return result
