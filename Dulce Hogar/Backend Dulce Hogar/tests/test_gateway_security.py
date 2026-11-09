import unittest
import httpx


class TestGatewaySecurity(unittest.TestCase):

    GATEWAY_URL = "http://127.0.0.1:8001/graphql"

    def test_pedido_sin_jwt(self):
        consulta = {
            "query": """
                query {
                    pedido(orderId: 7) {
                        id
                        clienteId
                        total
                    }
                }
            """
        }

        respuesta = httpx.post(
            self.GATEWAY_URL,
            json=consulta,
            timeout=5.0
        )

        self.assertEqual(respuesta.status_code, 200)

        datos = respuesta.json()

        self.assertIsNone(datos["data"]["pedido"])
        self.assertIn("errors", datos)

        self.assertIn(
            "Acceso denegado",
            datos["errors"][0]["message"]
        )
    
    def test_pedido_con_jwt_invalido(self):
        consulta = {
            "query": """
                query {
                    pedido(orderId: 7) {
                        id
                        clienteId
                        total
                    }
                }
            """
        }

        respuesta = httpx.post(
            self.GATEWAY_URL,
            json=consulta,
            headers={
                "Authorization": "Bearer token_invalido_de_prueba"
            },
            timeout=10.0
        )

        self.assertEqual(respuesta.status_code, 200)

        datos = respuesta.json()

        self.assertIsNone(datos["data"]["pedido"])
        self.assertIn("errors", datos)

        self.assertIn(
            "Acceso denegado",
            datos["errors"][0]["message"]
        )
    
    def test_cliente_no_puede_consultar_pedido_ajeno(self):
        import os

        token = os.getenv("TEST_CLIENT_JWT")

        if not token:
            self.skipTest(
                "Configura TEST_CLIENT_JWT con un token del cliente 3"
            )

        consulta = {
            "query": """
                query {
                    pedido(orderId: 6) {
                        id
                        clienteId
                        total
                    }
                }
            """
        }

        respuesta = httpx.post(
            self.GATEWAY_URL,
            json=consulta,
            headers={
                "Authorization": f"Bearer {token}"
            },
            timeout=10.0
        )

        self.assertEqual(respuesta.status_code, 200)

        datos = respuesta.json()

        self.assertIsNone(datos["data"]["pedido"])
        self.assertIn("errors", datos)
        self.assertIn(
            "El pedido no pertenece al usuario autenticado",
            datos["errors"][0]["message"]
        )


if __name__ == "__main__":
    unittest.main()
