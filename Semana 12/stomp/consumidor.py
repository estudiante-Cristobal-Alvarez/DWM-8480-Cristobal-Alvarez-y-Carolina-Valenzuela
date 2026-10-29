import argparse
import json
import time
import xml.etree.ElementTree as ET
import stomp

DESTINO = '/queue/pedidos'

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
            raise ValueError(f"Formato fijo inválido: longitud {len(cuerpo)} != 36")
        identificador = cuerpo[0:6]
        cliente = cuerpo[6:26].rstrip()
        monto = cuerpo[26:36]
        if not (identificador.isascii() and identificador.isdigit() and len(monto) == 10 and monto [:7].isdigit() and monto[7] == '.' and monto[8:].isdigit()):
            raise ValueError("Formato fijo inválido: campos no válidos.")
        return formato, {'id': identificador, 'cliente': cliente, 'monto': monto}
    
    if formato == 'json':
        return formato, json.loads(cuerpo)
    
    if formato == 'xml':
        raiz = ET.fromstring(cuerpo)
        if raiz.tag != 'pedido':
            raise ValueError(f"El nodo raiz de XTM debe ser <pedido>")
        return formato, {elemento.tag: elemento.text for elemento in raiz}
    raise ValueError(f"Formato desconocido: {formato}")


class Escuchador(stomp.ConnectionListener):
    def __init__(self, conexion):
        self.conexion = conexion

    def on_error(self, frame):
        print(f"Error recibido: {frame.body}")

    def on_disconnected(self):
        print("Desconectado stomp cerrada.")

    def on_message(self, frame):
        ack_id = frame.headers.get('ack')
        try: 
            formato, contenido = interpretar(frame.body, frame.headers)
            print(f"Mensaje recibido (formato: {formato} )")
            if isinstance (contenido, str):
                print(f"\n{contenido}")
            else:
                print(json.dumps(contenido, ensure_ascii=False, indent=2))
            self.conexion.ack(id=ack_id)
        except Exception as exc:
            print(f"Error al procesar el mensaje: {exc}")
            self.conexion.nack(id=ack_id, requeue=False)
    

def main():
    parser = argparse.ArgumentParser(description='Productor stomp para recibir parámetros')
    parser.add_argument('--host', default="127.0.0.1", type=str)
    parser.add_argument('--port', default=61613, type=int)
    parser.add_argument('--usuario', default="demo", type=str)
    parser.add_argument('--clave', default="demo123", type=str)
    args = parser.parse_args()
    conexion = stomp.Connection12([(args.host, args.port)], vhost="/")
    conexion.set_listener('pedidor', Escuchador(conexion))
    try:
        conexion.connect(args.usuario, args.clave, wait=True)
        conexion.subscribe(
            destination=DESTINO, 
            id= 'lector-pedidos', 
            ack='client-individual',
            headers={'prefetch-count': 1}
            )
        print(f"Escuchando {DESTINO}... Presione Ctrl+C para salir.")
        while conexion.is_connected():
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nDesconectando...")
    finally:
        if conexion.is_connected():
            conexion.disconnect()

if __name__ == "__main__":
    main()