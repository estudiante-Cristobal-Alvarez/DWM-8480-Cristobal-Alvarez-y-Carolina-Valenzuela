"""
Consumidor de pedidos de Dulce Hogar.

"""
import argparse
import json
import time
import xml.etree.ElementTree as ET
from decimal import Decimal, InvalidOperation
import stomp

from catalogo import CATALOGO

DESTINO = '/queue/pedidos'

# Lee un pedido en formato XML y lo convierte a un diccionario de Python.
def interpretar_xml(cuerpo):
    raiz = ET.fromstring(cuerpo)
    if raiz.tag != "pedido":
        raise ValueError("La raíz del XML debe ser <pedido>.")

    pedido = {}
    for nombre in ("id", "cliente", "tipo_pedido", "estado", "monto_total"):
        elemento = raiz.find(nombre)
        if elemento is not None:
            pedido[nombre] = elemento.text or ""

    productos_elemento = raiz.find("productos")
    productos = []
    if productos_elemento is not None:
        for producto_xml in productos_elemento.findall("producto"):
            producto = {}
            for campo in producto_xml:
                producto[campo.tag] = campo.text or ""
            productos.append(producto)
    pedido["productos"] = productos
    pedido.setdefault("moneda", "CLP")
    return pedido


def interpretar(cuerpo: str, headers: dict):
    formato = headers.get('x-formato', '').lower()
    tipo_mime = headers.get('content-type', '').lower()

    if not formato:
        if 'application/json' in tipo_mime:
            formato = 'json'
        elif 'application/xml' in tipo_mime or 'text/xml' in tipo_mime:
            formato = 'xml'
        else:
            formato = 'texto'

    if formato == 'texto':
        return formato, cuerpo

    if formato == 'fijo':
        if len(cuerpo) != 36:
            raise ValueError(f"Formato fijo inválido: longitud {len(cuerpo)}; se esperaban 36 caracteres.")
        identificador = cuerpo[0:6]
        cliente = cuerpo[6:26].rstrip()
        monto = cuerpo[26:36]
        if not (
            identificador.isascii()
            and identificador.isdigit()
            and monto[:7].isdigit()
            and monto[7] == "."
            and monto[8:].isdigit()
        ):
            raise ValueError("Formato fijo inválido: campos no válidos.")
        return formato, {
            'id': identificador,
            'cliente': cliente,
            'monto_total': monto,
        }
# Comprueba la estructura del mensaje
    if formato == 'json':
        contenido = json.loads(cuerpo)
        if not isinstance(contenido, dict):
            raise ValueError("El mensaje JSON debe ser un objeto.")
        return formato, contenido

    if formato == 'xml':
        return formato, interpretar_xml(cuerpo)

    raise ValueError(f"Formato desconocido: {formato}")

# Muestra el contenido de un pedido en la consola.
def mostrar_pedido(contenido):
    if isinstance(contenido, str):
        print(contenido)
        return

    print(f"Pedido N.°: {contenido.get('id', 'No indicado')}")
    print(f"Cliente: {contenido.get('cliente', 'No indicado')}")
    print(f"Estado: {contenido.get('estado', 'No indicado')}")
    print(f"Tipo: {contenido.get('tipo_pedido', 'No indicado')}")

    productos = contenido.get("productos", [])
    if productos:
        print("\nProductos:")
        for producto in productos:
            nombre = producto.get("nombre", producto.get("id_producto", "Producto"))
            cantidad = producto.get("cantidad", "?")
            unidad = producto.get("unidad", "")
            subtotal = producto.get("subtotal", "No indicado")
            print(f"  - {nombre}: {cantidad} {unidad} -- subtotal: ${subtotal} CLP")
    elif contenido.get("nota"):
        print(f"\n{contenido['nota']}")

    monto = contenido.get("monto_total", contenido.get("monto", "No indicado"))
    print(f"\nTOTAL: ${monto} CLP")


class Escuchador(stomp.ConnectionListener):
    def __init__(self, conexion):
        self.conexion = conexion

    def on_error(self, frame):
        print(f"Error recibido: {frame.body}")

    def on_disconnected(self):
        print("Conexión stomp cerrada.")

    def on_message(self, frame):
        ack_id = frame.headers.get("ack")
        try:
            formato, contenido = interpretar(frame.body, frame.headers)
            print(f"\nPedido recibido (formato: {formato})")
            mostrar_pedido(contenido)

            if not ack_id:
                raise ValueError(
                    "No se puede confirmar la recepción. El mensaje no tiene un identificador."
                )
            self.conexion.ack(id=ack_id)
            print("Mensaje confirmado correctamente.")
        except Exception as exc:
            print(f"Error al procesar el mensaje: {exc}")
            if ack_id:
                try:
                    self.conexion.nack(id=ack_id, requeue=False)
                    print("Mensaje rechazado. No se volverá a procesar.")
                except Exception as nack_exc:
                    print(f"No se pudo rechazar el mensaje: {nack_exc}")
            else:
                print("No se pudo rechazar el mensaje porque no tiene un identificador de confirmación.")


def main():
    parser = argparse.ArgumentParser(description="Consumidor stomp de pedidos de Dulce Hogar")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default=61613, type=int)
    parser.add_argument("--usuario", default="demo")
    parser.add_argument("--clave", default="demo123")
    args = parser.parse_args()

    conexion = stomp.Connection12([(args.host, args.port)], vhost="/")
    conexion.set_listener("dulce-hogar", Escuchador(conexion))

    try:
        conexion.connect(args.usuario, args.clave, wait=True)
        conexion.subscribe(
            destination=DESTINO,
            id="lector-pedidos",
            ack="client-individual",
            headers={"prefetch-count": 1},
        )
        print(f"Dulce Hogar escuchando {DESTINO}... Presione Ctrl+C para salir.")
        while conexion.is_connected():
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nDesconectando...")
    finally:
        if conexion.is_connected():
            conexion.disconnect()


if __name__ == "__main__":
    main()
