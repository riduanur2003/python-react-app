from fastapi import FastAPI, HTTPException, Depends
from typing import Annotated
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import SessionLocal, engine
import models
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins=[
    "http://localhost:3000"
]

# This is the part where we add 
app.add_middleware(
    CORSMiddleware, 
    allow_origins=origins,
    )

class TransactionBase(BaseModel):
    amount: float
    category: str
    description: str
    is_income: bool
    date: str

class TranscatoinModel(TransactionBase):
    id: int

    class Config:
        orm_mode = True


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

    

db_dependancy = Annotated[Session, Depends(get_db)]

models.Base.metadata.create_all(bind=engine)

@app.post("/transactions/", response_model = TranscatoinModel)
async def create_transaction(transaction: TransactionBase, db: db_dependancy):
    db_transaction = models.Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction