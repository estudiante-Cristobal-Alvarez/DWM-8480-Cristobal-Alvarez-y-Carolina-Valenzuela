from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Producto(Base):
    __tablename__ = "productos"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    nombre: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    categoria: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    precio: Mapped[int] = mapped_column(
        nullable=False
    )

    disponible: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )