
"use strict";
const CLAVE_CARRITO = "dulceHogarCarritoV2";

// Obtener los productos guardados
function obtenerCarrito() {
    try {
        const guardado = localStorage.getItem(CLAVE_CARRITO);
        const carrito = guardado ? JSON.parse(guardado) : [];

        if (!Array.isArray(carrito)) {
            return [];
        }

        return carrito.filter(item =>
            typeof item.id === "string" &&
            item.id.length > 0 &&
            typeof item.nombre === "string" &&
            typeof item.categoria === "string" &&
            typeof item.imagen === "string" &&
            Number.isFinite(item.precio) &&
            item.precio >= 0 &&
            Number.isInteger(item.cantidad) &&
            item.cantidad > 0 &&
            item.cantidad <= 99
        );

    } catch (error) {
        console.error("Error al recuperar el carrito:", error);
        return [];
    }
}


function guardarCarrito(carrito) {
    localStorage.setItem(
        CLAVE_CARRITO,
        JSON.stringify(carrito)
    );

    window.dispatchEvent(new Event("carritoActualizado"));
}


function agregarAlCarrito(producto, cantidad = 1) {

    if (
        !producto ||
        typeof producto.id !== "string" ||
        !producto.id ||
        typeof producto.nombre !== "string" ||
        typeof producto.categoria !== "string" ||
        typeof producto.imagen !== "string" ||
        !Number.isFinite(producto.precio) ||
        producto.precio < 0 ||
        !Number.isInteger(cantidad) ||
        cantidad < 1
    ) {
        throw new Error("Producto o cantidad inválida");
    }

    const carrito = obtenerCarrito();

    const existente = carrito.find(item =>
        item.id === producto.id &&
        item.categoria === producto.categoria
    );

    if (existente) {
        if (existente.cantidad + cantidad > 99) {
            throw new Error("Máximo 99 unidades por producto");
        }

        existente.cantidad += cantidad;

    } else {
        if (cantidad > 99) {
            throw new Error("Máximo 99 unidades por producto");
        }

        carrito.push({
            id: producto.id,
            nombre: producto.nombre,
            categoria: producto.categoria,
            precio: producto.precio,
            imagen: producto.imagen,
            cantidad: cantidad
        });
    }

    guardarCarrito(carrito);
}

function actualizarCantidad(id, categoria, cantidad) {

    if (!Number.isInteger(cantidad) ||
        cantidad < 0 ||
        cantidad > 99) {
        throw new Error("Cantidad inválida");
    }

    const carrito = obtenerCarrito();

    const item = carrito.find(producto =>
        producto.id === id &&
        producto.categoria === categoria
    );

    if (!item) return;

    if (cantidad === 0) {
        eliminarDelCarrito(id, categoria);
        return;
    }

    item.cantidad = cantidad;
    guardarCarrito(carrito);
}


function eliminarDelCarrito(id, categoria) {

    const carrito = obtenerCarrito().filter(producto =>
        !(producto.id === id && producto.categoria === categoria)
    );

    guardarCarrito(carrito);
}


function vaciarCarrito() {
    guardarCarrito([]);
}

function contarProductosCarrito() {
    return obtenerCarrito().reduce(
        (total, item) => total + item.cantidad,
        0
    );
}

function calcularTotalCarrito() {
    return obtenerCarrito().reduce(
        (total, item) => total + item.precio * item.cantidad,
        0
    );
}


 
// ==========================================
// INTERFAZ VISUAL DEL CARRITO
// ==========================================

function formatearPrecioCarrito(precio) {
    return "$" + precio.toLocaleString("es-CL");
}

function actualizarInterfazCarrito() {

    const contador = document.getElementById("contadorCarrito");
    const lista = document.getElementById("listaCarrito");
    const total = document.getElementById("totalCarrito");
    const botonVaciar = document.getElementById("vaciarCarritoBtn");

    if (!lista) return;

    const carrito = obtenerCarrito();

    if (contador) {
        contador.textContent = contarProductosCarrito();
    }

    lista.replaceChildren();

    if (carrito.length === 0) {

        const mensaje = document.createElement("p");
        mensaje.className = "text-center text-muted py-5";
        mensaje.textContent = "Tu carrito está vacío.";

        lista.appendChild(mensaje);

    } else {

        carrito.forEach((producto, indice) => {

            const fila = document.createElement("div");
            fila.className = "carrito-producto";

            // La estructura HTML es fija.
            // Los datos del producto se insertan como texto.
            fila.innerHTML = `
                <img class="carrito-imagen" alt="">
                <div class="carrito-informacion">
                    <h6 class="carrito-nombre"></h6>
                    <p class="carrito-precio"></p>
                    <div class="carrito-controles">
                        <button type="button"
                            data-accion="restar"
                            aria-label="Disminuir cantidad">−</button>
                        <span class="carrito-cantidad"></span>
                        <button type="button"
                            data-accion="sumar"
                            aria-label="Aumentar cantidad">+</button>
                    </div>
                    <button type="button"
                        class="carrito-eliminar"
                        data-accion="eliminar">
                        Eliminar
                    </button>
                </div>
                <strong class="carrito-subtotal"></strong>
            `;

            const imagen = fila.querySelector(".carrito-imagen");

            // Solo aceptar imágenes locales del catálogo.
            if (
                producto.imagen.startsWith("img/") &&
                !producto.imagen.includes("..") &&
                !producto.imagen.includes("\\")
            ) {
                imagen.src = producto.imagen;
            }

            imagen.alt = producto.nombre;

            fila.querySelector(".carrito-nombre").textContent =
                producto.nombre;

            fila.querySelector(".carrito-precio").textContent =
                formatearPrecioCarrito(producto.precio) + " c/u";

            fila.querySelector(".carrito-cantidad").textContent =
                producto.cantidad;

            fila.querySelector(".carrito-subtotal").textContent =
                formatearPrecioCarrito(
                    producto.precio * producto.cantidad
                );

            fila.querySelectorAll("button[data-accion]")
                .forEach(boton => {
                    boton.dataset.indice = indice;
                });

            fila.querySelector('[data-accion="sumar"]').disabled =
                producto.cantidad >= 99;

            lista.appendChild(fila);
        });
    }

    if (total) {
        total.textContent =
            formatearPrecioCarrito(calcularTotalCarrito());
    }

    if (botonVaciar) {
        botonVaciar.disabled = carrito.length === 0;
    }
}


document.addEventListener("DOMContentLoaded", () => {

    const lista = document.getElementById("listaCarrito");
    const botonVaciar = document.getElementById("vaciarCarritoBtn");

    actualizarInterfazCarrito();


    window.addEventListener(
        "carritoActualizado",
        actualizarInterfazCarrito
    );


    if (lista) {

        lista.addEventListener("click", (event) => {

            const boton = event.target.closest(
                "button[data-accion]"
            );

            if (!boton || !lista.contains(boton)) return;

            const indice = Number(boton.dataset.indice);
            const carrito = obtenerCarrito();

            if (!Number.isInteger(indice) || !carrito[indice]) {
                return;
            }

            const producto = carrito[indice];
            const accion = boton.dataset.accion;

            try {

                if (accion === "sumar") {
                    actualizarCantidad(
                        producto.id,
                        producto.categoria,
                        producto.cantidad + 1
                    );
                }

                if (accion === "restar") {
                    actualizarCantidad(
                        producto.id,
                        producto.categoria,
                        producto.cantidad - 1
                    );
                }

                if (accion === "eliminar") {
                    eliminarDelCarrito(
                        producto.id,
                        producto.categoria
                    );
                }

            } catch (error) {
                alert(error.message);
            }

        });
    }


    if (botonVaciar) {

        botonVaciar.addEventListener("click", () => {

            if (confirm("¿Quieres vaciar todo el carrito?")) {
                vaciarCarrito();
            }

        });
    }

});
