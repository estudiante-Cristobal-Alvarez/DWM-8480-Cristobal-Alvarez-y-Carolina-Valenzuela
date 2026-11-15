from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class Pedido(Base):
    __tablename__ = "pedidos"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    cliente_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    estado: Mapped[str] = mapped_column(
        String(30),
        default="pendiente",
        nullable=False
    )

    total: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )
    # nuevo
    metodo_pago: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    estado_pago: Mapped[str] = mapped_column(
        String(30),
        default="pendiente",  # "pendiente", "pagado", "rechazado"
        nullable=False
    )

    codigo_transaccion: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    detalles: Mapped[list["DetallePedido"]] = relationship(
        back_populates="pedido",
        cascade="all, delete-orphan"
    )
    #

class DetallePedido(Base):
    __tablename__ = "detalle_pedidos"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    pedido_id: Mapped[int] = mapped_column(
        ForeignKey("pedidos.id"),
        nullable=False
    )

    producto_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    cantidad: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    precio_unitario: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    subtotal: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    pedido: Mapped["Pedido"] = relationship(
        back_populates="detalles"
    )