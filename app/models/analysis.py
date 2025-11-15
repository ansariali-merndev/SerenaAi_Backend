from app.extensions import db
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, ForeignKey, DateTime
from datetime import datetime, timezone

class Analysis(db.Model):
    __tablename__ = "analysis"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    anger: Mapped[int] = mapped_column(Integer, nullable=False)
    anxiety: Mapped[int] = mapped_column(Integer, nullable=False)
    calmness: Mapped[int] = mapped_column(Integer, nullable=False)
    happiness: Mapped[int] = mapped_column(Integer, nullable=False)
    sadness: Mapped[int] = mapped_column(Integer, nullable=False)
    stress: Mapped[int] = mapped_column(Integer, nullable=False)
    
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc), 
        nullable=False
    )

    def to_dict(self):
        return {
            "id": self.id,
            "anger": self.anger,
            "anxiety": self.anxiety,
            "calmness": self.calmness,
            "happiness": self.happiness,
            "sadness": self.sadness,
            "stress": self.stress,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }