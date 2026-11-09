
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class Pago(Base):
    __tablename__ = "pagos"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    pedido_id: Mapped[int] = mapped_column(
        Integer,
        unique=True,
        nullable=False
    )

    monto: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    metodo_pago: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )

    estado: Mapped[str] = mapped_column(
        String(30),
        default="pendiente",
        nullable=False
    )
