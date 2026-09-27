document.addEventListener("DOMContentLoaded", () => {
    const bolleria = [
        {
            id: "medialunas",
            nombre: "Medialunas",
            precio: 1200,
            imagen: "img/bolleria/medialuna.png"
        },
        {
            id: "canoncitos-dulce-de-leche",
            nombre: "Cañoncitos con Manjar",
            precio: 1500,
            imagen: "img/bolleria/cañoncito.png"
        },
        {
            id: "libritos",
            nombre: "Libritos con Membrillo",
            precio: 1300,
            imagen: "img/bolleria/libritos.png"
        },
        {
            id: "pelotas-de-fraile",
            nombre: "Bolas de Fraile (Suspiros de monja)",
            precio: 1400,
            imagen: "img/bolleria/pelotasdefraile.png"
        },
        {
            id: "sacramentos",
            nombre: "Sacramentos",
            precio: 1500,
            imagen: "img/bolleria/sacramentos.png"
        }
    ];

    const contenedor = document.getElementById("lista-productos");

    if (!contenedor) {
        console.error("No se encontró el elemento #lista-productos en el HTML.");
        return;
    }

    function formatearPrecio(precio) {
        return "$" + precio.toLocaleString("es-CL");
    }

    function mostrarBolleria() {
        contenedor.innerHTML = "";

        bolleria.forEach(producto => {
            const tarjeta = document.createElement("div");
            tarjeta.className = "producto-card";

            tarjeta.innerHTML = `
                <img
                    src="${producto.imagen}"
                    class="producto-imagen"
                    alt="${producto.nombre}"
                >

                <div class="producto-info">
                    <h3 class="producto-nombre">
                        ${producto.nombre}
                    </h3>

                    <p class="producto-precio">
                        ${formatearPrecio(producto.precio)}
                    </p>

                    <a
                        href="producto.html?id=${producto.id}"
                        class="boton-producto"
                    >
                        Ver producto
                    </a>
                </div>
            `;

            contenedor.appendChild(tarjeta);
        });
    }

    mostrarBolleria();
});