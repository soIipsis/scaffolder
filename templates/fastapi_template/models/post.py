from typing import Optional
from fastapi_template.database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP, Boolean, text
from sqlalchemy.orm import relationship


class PostModel(Base):
    __tablename__ = "Posts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="TRUE", nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    owner_id = Column(
        Integer, ForeignKey("Users.id", ondelete="CASCADE"), nullable=False
    )

    relationship("UserModel")
