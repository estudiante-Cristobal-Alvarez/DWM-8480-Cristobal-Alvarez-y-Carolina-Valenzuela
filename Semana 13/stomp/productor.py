"""
Productor de pedidos para Dulce Hogar.
Ejemplos:
    python productor.py --formato texto --mensaje "Consulta por tortas"
    python productor.py --formato fijo --id 123 --cliente "Carolina Valenzuela" --monto 123.45
    python productor.py --formato json --cliente "Cristobal Alvarez" --producto marraqueta-grande:0.5 --producto medialunas:2
    python productor.py --formato xml --cliente "Juan Perez" --producto brownie:3
"""
import argparse
import json
from decimal import Decimal, InvalidOperation
import xml.etree.ElementTree as ET
import stomp

from catalogo import CATALOGO

DESTINO = '/queue/pedidos'


def construir_productos(selecciones):
    # Valida los productos y calcula los subtotales y el total.
    lineas = []
    total = Decimal("0.00")

    for seleccion in selecciones or []:
        try:
            identificador, cantidad_texto = seleccion.rsplit(":", 1)
            cantidad = Decimal(cantidad_texto)
        except (ValueError, InvalidOperation):
            raise ValueError(
                f"Producto inválido: '{seleccion}'. Usa el formato id:cantidad, por ejemplo medialunas:2."
            )

        if identificador not in CATALOGO:
            raise ValueError(
                f"Producto '{identificador}' no existe en el catálogo de Dulce Hogar."
            )
        if not cantidad.is_finite() or cantidad <= 0:
            raise ValueError(f"La cantidad de '{identificador}' debe ser mayor que cero.")

        producto = CATALOGO[identificador]
        precio = Decimal(producto["precio"])
        subtotal = (precio * cantidad).quantize(Decimal("0.01"))
        total += subtotal

        lineas.append({
            'id_producto': identificador,
            'nombre': producto["nombre"],
            'categoria': producto["categoria"],
            'cantidad': str(cantidad.normalize()),
            'unidad': producto["unidad"],
            'precio_unitario': str(precio),
            'subtotal': str(subtotal),
        })

    return lineas, total.quantize(Decimal("0.01"))


def construir_mensaje(formato, pedido, texto):
    if formato == 'texto':
        return texto, 'text/plain; charset=utf-8'

    if formato == 'fijo':
        # Formato fijo de 36 caracteres: ID[6], CLIENTE[20], MONTO[10].
        identificador = str(pedido["id"])
        cliente = str(pedido["cliente"])
        monto = Decimal(str(pedido["monto_total"]))
        monto_campo = f"{monto:010.2f}"

        if not (identificador.isascii() and identificador.isdigit() and len(identificador) <= 6):
            raise ValueError("El ID del pedido debe tener hasta 6 dígitos.")
        if not cliente.isascii() or len(cliente) > 20:
            raise ValueError("En formato fijo, el cliente debe ser ASCII y tener hasta 20 caracteres.")
        if monto < 0 or len(monto_campo) != 10:
            raise ValueError("El monto debe caber en 10 caracteres, con 2 decimales.")
        return f"{identificador.zfill(6)}{cliente:<20}{monto_campo}", 'text/plain; charset=utf-8'
    if formato == 'json':
        return json.dumps(pedido, ensure_ascii=False), 'application/json; charset=utf-8'

    if formato == 'xml':
        raiz = ET.Element("pedido")
        for clave in ("id", "cliente", "tipo_pedido", "estado", "monto_total"):
            ET.SubElement(raiz, clave).text = str(pedido[clave])
        productos_xml = ET.SubElement(raiz, "productos")
        for producto in pedido["productos"]:
            producto_xml = ET.SubElement(productos_xml, "producto")
            for clave, valor in producto.items():
                ET.SubElement(producto_xml, clave).text = str(valor)
        return ET.tostring(raiz, encoding="unicode"), 'application/xml; charset=utf-8'

    raise ValueError(f"Formato desconocido: {formato}")


def main():
    parser = argparse.ArgumentParser(description="Productor STOMP de pedidos de Dulce Hogar")
    parser.add_argument("--formato", choices=["texto", "fijo", "xml", "json"], required=True)
    parser.add_argument("--mensaje", default="Hola desde Dulce Hogar")
    parser.add_argument("--id", default=123, type=int)
    parser.add_argument("--cliente", default="Cliente Dulce Hogar")
    parser.add_argument(
        "--producto", action="append", default=[],
        help="Producto y cantidad en formato id:cantidad. Se puede repetir. Panadería: cantidad en kg; pastelería/bollería: unidades."
    )
    parser.add_argument("--monto", default="0.00", help="Monto manual para formato fijo o pedidos sin productos.")
    parser.add_argument("--tipo-pedido", choices=["retiro_en_tienda", "despacho"], default="retiro_en_tienda")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default=61613, type=int)
    parser.add_argument("--usuario", default="demo")
    parser.add_argument("--clave", default="demo123")
    args = parser.parse_args()

    if args.id < 0 or args.id > 999999:
        parser.error("El ID debe estar entre 0 y 999999.")

    try:
        monto_manual = Decimal(str(args.monto))
        if not monto_manual.is_finite() or monto_manual < 0:
            raise ValueError("El monto debe ser un número finito y no negativo.")
        productos, total = construir_productos(args.producto)
    except (ValueError, InvalidOperation) as exc:
        parser.error(str(exc))

    # Si se seleccionaron productos, el total se calcula desde el catálogo.
    # Si no se seleccionaron, se conserva --monto para compatibilidad con las pruebas antiguas.
    monto_total = total if productos else monto_manual.quantize(Decimal("0.01"))

    pedido = {
        "id": args.id,
        "cliente": args.cliente,
        "productos": productos,
        "tipo_pedido": args.tipo_pedido,
        "estado": "recibido",
        "monto_total": str(monto_total),
        "moneda": "CLP",
    }

    try:
        cuerpo, mime = construir_mensaje(args.formato, pedido, args.mensaje)
    except (ValueError, InvalidOperation) as exc:
        parser.error(str(exc))

    conexion = stomp.Connection12([(args.host, args.port)], vhost="/")  # type: ignore[attr-defined]
    try:
        conexion.connect(args.usuario, args.clave, wait=True)
        conexion.send(
            destination=DESTINO,
            body=cuerpo,
            headers={
                "content-type": mime,
                "x-formato": args.formato,
                "persistent": "true",
            },
        )
        print(f"Pedido enviado a {DESTINO} con formato {args.formato}:")
        print(cuerpo)
    finally:
        if conexion.is_connected():
            conexion.disconnect()


if __name__ == "__main__":
    main()
