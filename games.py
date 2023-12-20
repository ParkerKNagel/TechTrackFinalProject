from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

class Game(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    publisher: Mapped[str] = mapped_column(String)
    console: Mapped[str] = mapped_column(String)
    genre: Mapped[str] = mapped_column(String)
    rating: Mapped[str] = mapped_column(String)
    score: Mapped[str] = mapped_column(String)
