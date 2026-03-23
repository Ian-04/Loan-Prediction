from sqlalchemy.orm import Session
import models
import schemas

# Getting user from DB
def get_users(db: Session, search: str = None):
    query = db.query(models.Loans)
    if search:
        query = query.filter(models.Loans.name.ilike(f"%{search}%") | models.Loans.email.ilike(f"%{search}%"))
    return query.all()