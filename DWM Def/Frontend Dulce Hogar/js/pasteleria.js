document.addEventListener("DOMContentLoaded", () => {
    const pasteles = [
        {
            id: "torta-selva-negra",
            nombre: "Torta Selva Negra",
            precio: 12990,
            imagen: "img/pasteleria/selvanegra.png"
        },
        {
            id: "pie-de-limon",
            nombre: "Pie de Limón",
            precio: 8990,
            imagen: "img/pasteleria/piedelimon.png"
        },
        {
            id: "torta-tres-leches",
            nombre: "Torta Tres Leches",
            precio: 11500,
            imagen: "img/pasteleria/tresleches.png"
        },
        {
            id: "tartaleta-frutas",
            nombre: "Tartaleta de Frutas",
            precio: 9500,
            imagen: "img/pasteleria/tartaleta.png"
        },
        {
            id: "brownie",
            nombre: "Brownie",
            precio: 1500,
            imagen: "img/pasteleria/brownie.png"
        },
        {
            id: "tiramisu",
            nombre: "Tiramisú",
            precio: 9500,
            imagen: "img/pasteleria/tiramisu.png"
        },
        {
            id: "cheescake-frambuesa",
            nombre: "Cheesecake de frambuesa",
            precio: 12000,
            imagen: "img/pasteleria/cheesecakedeframbuesa.png"
        },
        {
            id: "rollos-canela",
            nombre: "Rollos de canela",
            precio: 5000,
            imagen: "img/pasteleria/rollosdecanela.png"
        },
        {
            id: "kuchen-manzana",
            nombre: "Kuchen de manzana",
            precio: 11500,
            imagen: "img/pasteleria/kuchendemanzana.png"
        },
        {
            id: "queque-vainilla",
            nombre: "Queque de vainilla",
            precio: 5500,
            imagen: "img/pasteleria/quequedevainilla.png"
        },
        {
            id: "empolvados",
            nombre: "Empolvados",
            precio: 500,
            imagen: "img/pasteleria/empolvados.png"
        },
        {
            id: "chilenitos",
            nombre: "Chilenitos",
            precio: 500,
            imagen: "img/pasteleria/chilenitos.png"
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

    function mostrarPasteles() {
        contenedor.innerHTML = "";

        pasteles.forEach(pastel => {
            const tarjeta = document.createElement("div");
            tarjeta.className = "producto-card";

            tarjeta.innerHTML = `
                <img
                    src="${pastel.imagen}"
                    class="producto-imagen"
                    alt="${pastel.nombre}"
                >

                <div class="producto-info">
                    <h3 class="producto-nombre">
                        ${pastel.nombre}
                    </h3>

                    <p class="producto-precio">
                        ${formatearPrecio(pastel.precio)}
                    </p>

                    <a
                        href="producto.html?id=${pastel.id}"
                        class="boton-producto"
                    >
                        Ver producto
                    </a>
                </div>
            `;

            contenedor.appendChild(tarjeta);
        });
    }

    mostrarPasteles();
});