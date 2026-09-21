const productos = [
    {
        id: 1,
        nombre: "Pan amasado",
        categoria: "Pan",
        precio: 1200,
        descripcion: "Pan tradicional, suave y recién horneado.",
        icono: "🥖"
    },
    {
        id: 2,
        nombre: "Hallulla",
        categoria: "Pan",
        precio: 1500,
        descripcion: "Hallullas suaves ideales para desayuno y once.",
        icono: "🍞"
    },
    {
        id: 3,
        nombre: "Marraqueta",
        categoria: "Pan",
        precio: 1300,
        descripcion: "Marraqueta crujiente preparada diariamente.",
        icono: "🥖"
    },
    {
        id: 4,
        nombre: "Torta de chocolate",
        categoria: "Pastelería",
        precio: 15990,
        descripcion: "Torta de chocolate preparada para compartir.",
        icono: "🍰"
    },
    {
        id: 5,
        nombre: "Pie de limón",
        categoria: "Pastelería",
        precio: 9990,
        descripcion: "Pie con crema de limón y cubierta de merengue.",
        icono: "🥧"
    },
    {
        id: 6,
        nombre: "Empanada",
        categoria: "Salado",
        precio: 2500,
        descripcion: "Empanada horneada preparada durante el día.",
        icono: "🥟"
    }
];


const parametros = new URLSearchParams(
    window.location.search
);

const id = Number(
    parametros.get("id")
);


const producto = productos.find(
    function (item) {
        return item.id === id;
    }
);


const contenedor =
    document.getElementById("detalle-producto");


if (producto) {

    contenedor.innerHTML = `

        <div class="row justify-content-center">

            <div class="col-md-8">

                <div class="card detalle">

                    <div class="producto-grande">
                        ${producto.icono}
                    </div>

                    <div class="card-body">

                        <h2>
                            ${producto.nombre}
                        </h2>

                        <p>
                            <strong>Categoría:</strong>
                            ${producto.categoria}
                        </p>

                        <p>
                            ${producto.descripcion}
                        </p>

                        <p class="precio">
                            $${producto.precio.toLocaleString("es-CL")}
                        </p>

                        <a
                            href="productos.html"
                            class="btn boton-principal"
                        >
                            Volver al catálogo
                        </a>

                    </div>

                </div>

            </div>

        </div>
    `;

} else {

    contenedor.innerHTML = `

        <div class="alert alert-danger">

            Producto no encontrado.

            <a href="productos.html">
                Volver al catálogo
            </a>

        </div>
    `;
}