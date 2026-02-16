from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from datetime import datetime
from .base import BaseModel


class Log(BaseModel):
    """Логи действий пользователей и системы"""
    __tablename__ = "log"

    user_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'), nullable=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    action = Column(String(50), nullable=False)  # 'load', 'generate', 'update', etc.
    item_id = Column(String(36))
    message = Column(Text)
    status = Column(String(20))  # 'pending', 'completed', 'error'
    
    def __repr__(self):
        return f"<Log(action={self.action}, status={self.status})>"
