from fastapi import FastAPI, Depends, HTTPException
from typing import Annotated
from .crud import *
from .database import SessionLocal, engine, Base
from .schemas import *

Base.metadata.create_all(bind=engine)
app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/client/{sn}", response_model=ClientSchema)
def get_client(name: str, db: Session = Depends(get_db)):
    db_client = get_client_by_name(db, name=name)
    if not db_client:
        raise HTTPException(status_code=409, detail="client don't exist")
    return db_client


@app.post("/client/", response_model=ClientSchema)
def post_client(client: ClientSchema, db: Session = Depends(get_db)):
    db_client = get_client_by_name(db, name=client.name)
    if db_client:
        raise HTTPException(status_code=409, detail="client already exist")
    return create_client(db=db, client=client)


@app.get("/book/{sn}", response_model=BookSchema)
def get_book(serial_number: str, db: Session = Depends(get_db)):
    db_book = get_book_by_serial_number(db, serial_number=serial_number)
    if not db_book:
        raise HTTPException(status_code=409, detail="book don't exist")
    return db_book


@app.post("/book/", response_model=BookSchema)
def post_book(book: BookSchema, db: Session = Depends(get_db)):
    db_book = get_book_by_serial_number(db, serial_number=book.serial_number)
    if db_book:
        raise HTTPException(status_code=409, detail="book already exist")
    return create_book(db=db, book=book)


@app.put("/book/{sn}{client_id}", response_model=BookSchema)
def update_book_status(book: BookSchema, db: Session = Depends(get_db)):
    db_client = db.query(Client).filter(Client.id == book.client_id).one_or_none()
    db_book = db.query(Book).filter(Book.serial_number == book.serial_number).one_or_none()

    if db_client or book.client_id is None and db_book:
        for var, value in vars(book).items():
            setattr(db_book, var, value)

        db.commit()
        db.refresh(db_book)
        return db_book

    else:
        raise HTTPException(status_code=409, detail="book or client don't exist")


@app.delete("/book/{sn}")
def delete_book(serial_number: str, db: Session = Depends(get_db)):
    db_book = del_book(db, serial_number=serial_number)
    if not db_book:
        raise HTTPException(status_code=409, detail="book don't exist")
    return {"message": "Item deleted successfully"}


@app.get("/books/")
def get_books_list(db: Annotated[Session, Depends(get_db)], page: int = 1, size: int = 10):
    return paginate_books_list(db, page, size)
