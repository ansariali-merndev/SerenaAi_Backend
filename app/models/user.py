from app.extensions import db
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import Integer, String, DateTime
from datetime import datetime, timezone

class User(db.Model):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    firstname: Mapped[str] = mapped_column(String(155), nullable=False)
    lastname: Mapped[str] = mapped_column(String(255), nullable=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(), default=datetime.now(timezone.utc), nullable=False)
    
