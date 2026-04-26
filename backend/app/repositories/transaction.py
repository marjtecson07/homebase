from typing import Any, List

from sqlalchemy.orm import Session

from app.models.transaction import Transaction
from app.repositories.base import BaseRepository


class TransactionRepository(BaseRepository[Transaction]):
    def __init__(self, db: Session):
        super().__init__(Transaction, db)

    def get_by_household(self, household_id: Any) -> List[Transaction]:
        return (
            self.db.query(Transaction)
            .filter(Transaction.household_id == household_id)
            .all()
        )

    def get_by_user(self, user_id: Any) -> List[Transaction]:
        return (
            self.db.query(Transaction)
            .filter(Transaction.created_by_id == user_id)
            .all()
        )

    def get_shared(self, household_id: Any) -> List[Transaction]:
        return (
            self.db.query(Transaction)
            .filter(Transaction.household_id == household_id, Transaction.is_shared)
            .all()
        )
