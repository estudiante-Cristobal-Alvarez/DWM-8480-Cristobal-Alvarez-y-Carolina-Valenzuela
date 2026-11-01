# Texto Libre
# python productor.py --formato texto --mensaje "Hola mundo stomp"
# Texto Ancho de Fijo
# python productor.py --formato fijo --id 123 --cliente "Carolina Valenzuela" --monto 123.45
# XML
# python productor.py --formato xml --id 123 --cliente "Carolina Valenzuela" --monto 123.45
# JSON
# python productor.py --formato json --id 123 --cliente "Carolina Valenzuela" --monto 123.45

import stomp
import argparse
import json
from decimal import Decimal, InvalidOperation
import xml.etree.ElementTree as ET 

DESTINO = '/queue/pedidos'
def construir_mensaje(formato: str, pedido: dict, texto: str) -> tuple[str, str]:
    if formato == 'texto':
        return texto, 'text/plain; charset=utf-8'
    if formato == 'fijo':
        # Contrato fixed 36 chaars: ID[6], CLIENTE[20], MONTO[10]
        identificador = str(pedido['id'])
        cliente = str(pedido['cliente'])
        monto = Decimal(pedido['monto'])
        monto_campo = f"{monto:010.2f}" #str format de un decimal con 10 caracteres, 2 decimales, rellenado con ceros a la izquierda
        if not (identificador.isascii() and identificador.isdigit() and len(identificador) <= 6):
            raise ValueError("ID debe ser un número de hasta 6 dígitos.")
        if len(cliente) > 20 or any(ord(c) > 127 for c in cliente):
            raise ValueError("Cliente debe ser un texto ASCII de hasta 20 caracteres.")
        if monto < 0 or len(monto_campo) != 10:
            raise ValueError("Monto debe ser un número positivo entre 0 y 99999999.99.")
        return f"{identificador.zfill(6)}{cliente:<20}{monto_campo}", 'text/plain; charset=utf-8'
    if formato == 'json':
        return json.dumps(pedido, ensure_ascii=False), 'application/json; charset=utf-8'
    if formato == 'xml':
        raiz = ET.Element('pedido')
        for clave, valor in pedido.items():
            ET.SubElement(raiz, clave).text = str(valor)
        return ET.tostring(raiz, encoding ='unicode'), 'application/xml; charset=utf-8'
    raise ValueError(f"Formato desconocido: {formato}")
           
    

def main():
    parser = argparse.ArgumentParser(description='Productor stomp para recibir parámetros')
    parser.add_argument('--formato', choices=['texto', 'fijo', 'xml', 'json'], required=True)
    parser.add_argument('--mensaje', default= "Hola desde stomp")

    parser.add_argument('--id', default="123", type=int)
    parser.add_argument('--cliente', default="Carolina Valenzuela", type=str)
    parser.add_argument('--monto', default=123.45, type=float)
    parser.add_argument('--host', default="127.0.0.1", type=str)
    parser.add_argument('--port', default=61613, type=int)
    parser.add_argument('--usuario', default="demo", type=str)
    parser.add_argument('--clave', default="demo123", type=str)
    args = parser.parse_args()


    try:
        monto = Decimal(str(args.monto))
        if not monto.is_finite():
            raise ValueError("Monto debe ser un número finito.")
    except InvalidOperation as exc:
        parser.error(f"Error al procesar el monto: {args.monto}")
    pedido = {
        "id": args.id,
        "cliente": args.cliente,
        "monto": str(monto)
    }

    try:
        cuerpo, mime = construir_mensaje(args.formato, pedido, args.mensaje)
    except ValueError as exc:
        parser.error(str(exc))

    #Enviar mensaje al broker stomp
    conexion = stomp.Connection12([(args.host, args.port)], vhost="/")

    try:
        conexion.connect(args.usuario, args.clave, wait=True)
        conexion.send(
            destination=DESTINO, 
            body=cuerpo, 
            headers={
                'content-type': mime,
                'x-formato': args.formato,
                'persistent': 'true',
            } 
        )
        print(f"Mensaje enviado a {DESTINO} con formato {args.formato}):\n{cuerpo}")
    finally:
        if conexion.is_connected():
            conexion.disconnect()



if __name__ == '__main__':
    main()