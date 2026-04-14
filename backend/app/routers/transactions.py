from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from uuid import UUID
from app.database import get_db
from app.schemas.transaction import (TransactionCreate, TransactionUpdate, 
                                      TransactionResponse)
from app.services.transaction import TransactionService
from app.models.user import User
from app.auth import get_current_user

router = APIRouter(prefix="/transactions", tags=["Transactions"])

@router.post("/", response_model=TransactionResponse,
             status_code=status.HTTP_201_CREATED)
def create_transaction(
    transaction_data: TransactionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = TransactionService(db)
    return service.create_transaction(transaction_data, current_user)

@router.get("/", response_model=list[TransactionResponse])
def get_transactions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = TransactionService(db)
    return service.get_household_transactions(current_user)

@router.get("/{transaction_id}", response_model=TransactionResponse)
def get_transaction(
    transaction_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = TransactionService(db)
    return service.get_transaction(transaction_id, current_user)

@router.put("/{transaction_id}", response_model=TransactionResponse)
def update_transaction(
    transaction_id: UUID,
    transaction_data: TransactionUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = TransactionService(db)
    return service.update_transaction(transaction_id, transaction_data, 
                                       current_user)

@router.delete("/{transaction_id}", 
               status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(
    transaction_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = TransactionService(db)
    service.delete_transaction(transaction_id, current_user)