from sqlalchemy import Column, String, Boolean, Enum
import enum
from .base import BaseModel


class UserRole(str, enum.Enum):
    """Роли пользователей"""
    ADMIN = "admin"
    USER = "user"


class User(BaseModel):
    __tablename__ = "users"

    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    
    is_active = Column(Boolean, default=True, nullable=False)
    role = Column(Enum(UserRole, native_enum=False), default=UserRole.USER, nullable=False)

    def __repr__(self):
        return f"<User(email={self.email}, role={self.role})>"
