from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from uuid import UUID
from app.repositories.transaction import TransactionRepository
from app.models.transaction import Transaction
from app.models.user import User
from app.schemas.transaction import TransactionCreate, TransactionUpdate

class TransactionService:
    def __init__(self, db: Session):
        self.transaction_repo = TransactionRepository(db)

    def create_transaction(self, transaction_data: TransactionCreate,
                           current_user: User) -> Transaction:
        transaction = Transaction(
            **transaction_data.model_dump(),
            household_id=current_user.household_id,
            created_by_id=current_user.id
        )
        return self.transaction_repo.create(transaction)

    def get_household_transactions(self, 
                                   current_user: User) -> list[Transaction]:
        return self.transaction_repo.get_by_household(
            current_user.household_id
        )

    def get_transaction(self, transaction_id: UUID, 
                        current_user: User) -> Transaction:
        transaction = self.transaction_repo.get_by_id(transaction_id)
        if transaction is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction not found"
            )
        if str(transaction.household_id) != str(current_user.household_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction not found"
            )
        return transaction

    def update_transaction(self, transaction_id: UUID,
                           transaction_data: TransactionUpdate,
                           current_user: User) -> Transaction:
        transaction = self.get_transaction(transaction_id, current_user)
        for field, value in transaction_data.model_dump(
            exclude_unset=True
        ).items():
            setattr(transaction, field, value)
        return self.transaction_repo.update(transaction)

    def delete_transaction(self, transaction_id: UUID, 
                           current_user: User) -> None:
        transaction = self.get_transaction(transaction_id, current_user)
        self.transaction_repo.delete(transaction)