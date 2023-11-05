from fastapi import FastAPI, HTTPException, Response, status, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import models.models as models
from db.database import engine, SessionLocal
from schemas.schemas import Book
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message" : "hello World"}

@app.get("/players")
def root():
    return {"message" : "hello players. best of luck"}

@app.get("/books")
def get_books(db: Session = Depends(get_db)):
    books = db.query(models.Books).all()
    print(books)
    return {"data" : books}

@app.get("/books/{id}")
def get_book(id: int, db: Session = Depends(get_db)):
    book = db.query(models.Books).filter(models.Books.id == id).first()
    if not book:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail = f"Book with id: {id} was not found")
    return {"data": book}

@app.post("/books", status_code = status.HTTP_201_CREATED)
def create_book(book: Book, db: Session = Depends(get_db)):
    book_model = models.Books()
    book_model.title = book.title
    book_model.author = book.author
    book_model.description = book.description
    book_model.rating = book.rating

    db.add(book_model)
    db.commit()
    
    return {"data": book}

@app.put("/books/{id}")
def update_book(id: int, book: Book, db: Session = Depends(get_db)):
    book_model = db.query(models.Books).filter(models.Books.id == id).first()
    if not book_model:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail = f"Post with id: {id} was not found")
    
    book_model.title = book.title
    book_model.author = book.author
    book_model.description = book.description
    book_model.rating = book.rating
    
    db.add(book_model)
    db.commit()
    
    return {"data": book}

@app.delete("/books/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_book(id: int, db: Session = Depends(get_db)):
    book_model = db.query(models.Books).filter(models.Books.id == id).first()
    if not book_model:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail = f"Book with id: {id} does not exists")
    
    db.query(models.Books).filter(models.Books.id == id).delete()
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)