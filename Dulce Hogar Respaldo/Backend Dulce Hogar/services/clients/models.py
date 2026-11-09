from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class Cliente(Base):
    __tablename__ = "clientes"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    nombre: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    correo: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        index=True,
        nullable=False
    )

    telefono: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True
    )

    direccion: Mapped[str | None] = mapped_column(
        String(250),
        nullable=True
    )