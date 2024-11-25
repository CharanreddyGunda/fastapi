from database import Base
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

class Post(Base):
    __tablename__ = 'post'

    id:Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title:Mapped[str] = mapped_column(String, nullable=False, index=True)
    content:Mapped[str] = mapped_column(String, nullable=False, index=True)
    published:Mapped[bool] = mapped_column(Boolean, default=True)

    
