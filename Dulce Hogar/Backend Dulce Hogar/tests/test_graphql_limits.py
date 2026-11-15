import unittest

from graphql import build_schema, parse, validate

from services.gateway.graphql_limits import MaxFieldsRule


class TestGraphQLLimits(unittest.TestCase):

    def setUp(self):
        self.schema = build_schema("type Query { producto: Int }")

    def test_consulta_valida(self):
        consulta = "{ producto }"

        errores = validate(
            self.schema,
            parse(consulta),
            rules=[MaxFieldsRule]
        )

        self.assertEqual(errores, [])

    def test_consulta_supera_50_campos(self):
        campos = " ".join(
            f"campo{i}: producto"
            for i in range(51)
        )

        consulta = "{ " + campos + " }"

        errores = validate(
            self.schema,
            parse(consulta),
            rules=[MaxFieldsRule]
        )

        self.assertEqual(len(errores), 1)
        self.assertIn(
            "supera el limite de 50 campos",
            errores[0].message
        )
    
    def test_fragmento_supera_50_campos(self):
        campos = " ".join(
            f"campo{i}: producto"
            for i in range(51)
        )

        consulta = f"""
        query {{
            ...CamposProducto
        }}

        fragment CamposProducto on Query {{
            {campos}
        }}
        """

        errores = validate(
            self.schema,
            parse(consulta),
            rules=[MaxFieldsRule]
        )

        self.assertEqual(len(errores), 1)
        self.assertIn(
            "supera el limite de 50 campos",
            errores[0].message
        )


if __name__ == "__main__":
    unittest.main()
