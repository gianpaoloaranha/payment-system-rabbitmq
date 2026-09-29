from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database import Base


class RevokedToken(Base):
    """Tokens invalidados via logout. Como o JWT é stateless, o logout só
    funciona se guardarmos o `jti` do token até ele expirar."""

    __tablename__ = "revoked_tokens"

    jti: Mapped[str] = mapped_column(String(64), primary_key=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
