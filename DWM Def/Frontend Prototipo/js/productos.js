const productos = [
    {
        id: "hamburguesa-brioche",
        nombre: "Hamburguesa Brioche",
        categoria: "panaderia",
        precio: 3690,
        imagen: "img/panes/Pan Hamburguesa Brioche Granel 3690 x kg.png"
    },
    {
        id: "hogaza-multi-wholegrain",
        nombre: "Hogaza Multi Wholegrain 700 g",
        categoria: "panaderia",
        precio: 4700,
        imagen: "img/panes/Pan Hogaza Multi Wholegrain 700 g 4700 x kg.png"
    },
    {
        id: "hoja",
        nombre: "Hoja Granel",
        categoria: "panaderia",
        precio: 5490,
        imagen: "img/panes/Pan Hoja Granel 5490 x kg.png"
    },
    {
        id: "hot-dog",
        nombre: "Hot Dog Granel",
        categoria: "panaderia",
        precio: 3290,
        imagen: "img/panes/Pan Hot Dog Granel 3290 x kg.png"
    },
    {
        id: "landbrot",
        nombre: "Pan Landbrot 800 g",
        categoria: "panaderia",
        precio: 4363,
        imagen: "img/panes/Pan Landbrot 800 g 4363 x kg.png"
    },
    {
        id: "marraqueta-grande",
        nombre: "Marraqueta Grande",
        categoria: "panaderia",
        precio: 2290,
        imagen: "img/panes/Pan Marraqueta Grande 2290 x kg.jpg"
    },
    {
        id: "amasado",
        nombre: "Amasado Granel",
        categoria: "panaderia",
        precio: 3290,
        imagen: "img/panes/Pan Amasado Granel 3290 x kg.png"
    },
    {
        id: "baguetin-rustico",
        nombre: "Baguetín Rústico Granel",
        categoria: "panaderia",
        precio: 3490,
        imagen: "img/panes/Pan Baguetín Rústico Granel 3690 x kg.png"
    },
    {
        id: "baguette-rustico",
        nombre: "Baguette Rústico Tradicional",
        categoria: "panaderia",
        precio: 4967,
        imagen: "img/panes/Pan Baguette Rústico Tradicional 1 un. 4967 x kg.png"
    },
    {
        id: "bocado-dama",
        nombre: "Bocado de Dama Granel",
        categoria: "panaderia",
        precio: 4490,
        imagen: "img/panes/Pan Bocado de Dama Granel 4490 x kg.png"
    },
    {
        id: "campo-cinco-granos",
        nombre: "Campo 5 Granos Granel",
        categoria: "panaderia",
        precio: 5978,
        imagen: "img/panes/Pan Campo 5 Granos Granel 5978 x kg.png"
    },
    {
        id: "ciabatta-famiglia",
        nombre: "Ciabatta Famiglia Artesanal",
        categoria: "panaderia",
        precio: 3490,
        imagen: "img/panes/Pan Ciabatta Famiglia Artesanal 3490 x kg.png"
    },
    {
        id: "ciabatta",
        nombre: "Ciabatta Granel",
        categoria: "panaderia",
        precio: 3490,
        imagen: "img/panes/Pan Ciabatta Granel 3490 x kg.jpg"
    },
    {
        id: "ciabatta-integral",
        nombre: "Ciabatta Integral Granel",
        categoria: "panaderia",
        precio: 3490,
        imagen: "img/panes/Pan Ciabatta Integral Granel 3490 x kg.png"
    },
    {
        id: "coliza",
        nombre: "Coliza Granel",
        categoria: "panaderia",
        precio: 3490,
        imagen: "img/panes/Pan Coliza Granel 3490 x kg.png"
    },
    {
        id: "coliza-peruana",
        nombre: "Coliza Peruana Granel",
        categoria: "panaderia",
        precio: 3690,
        imagen: "img/panes/Pan Coliza Peruana Granel 3690 x kg.png"
    },
    {
        id: "pan-hamburguesa",
        nombre: "Hamburguesa Granel",
        categoria: "panaderia",
        precio: 3290,
        imagen: "img/panes/Pan de Hamburguesa Granel 3290 x kg.png"
    },
    {
        id: "hallulla-delgada",
        nombre: "Hallulla Delgada Granel",
        categoria: "panaderia",
        precio: 2990,
        imagen: "img/panes/Pan Hallulla Delgada Granel 2290 x kg.png"
    },
    {
        id: "hallulla",
        nombre: "Hallulla Granel",
        categoria: "panaderia",
        precio: 2190,
        imagen: "img/panes/Pan Hallulla Granel 2190 x kg.png"
    },
    {
        id: "hallulla-integral",
        nombre: "Hallulla Integral Linaza Granel",
        categoria: "panaderia",
        precio: 2990,
        imagen: "img/panes/Pan Hallulla Integral Linaza Granel 2990 x kg.png"
    },
    {
        id: "rositas",
        nombre: "Rositas Granel",
        categoria: "panaderia",
        precio: 2990,
        imagen: "img/panes/Pan Rositas Granel 2990 x kg.png"
    },
    {
        id: "rustikal-brot",
        nombre: "Rustikal Brot 850 g",
        categoria: "panaderia",
        precio: 4341,
        imagen: "img/panes/Pan Rustikal Brot 850 g 4341 x kg.png"
    },
    {
        id: "toscano",
        nombre: "Toscano Granel",
        categoria: "panaderia",
        precio: 3490,
        imagen: "img/panes/Pan Toscano Granel 3490 x kg.png"
    },
    {
        id: "marraqueta-wholegrain",
        nombre: "Marraqueta Wholegrain Granel",
        categoria: "panaderia",
        precio: 3290,
        imagen: "img/panes/Pan Marraqueta Wholegrain Granel 3290 x kg.png"
    },
    {
        id: "pita-blanco",
        nombre: "Pita Blanco Granel",
        categoria: "panaderia",
        precio: 3490,
        imagen: "img/panes/Pan Pita Blanco Granel 3490 x kg.png"
    },
    {
        id: "pita-integral",
        nombre: "Pita Integral Chía Linaza Granel",
        categoria: "panaderia",
        precio: 3490,
        imagen: "img/panes/Pan Pita Integral Chía Linaza Granel 3490 x kg.png"
    }
];


const parametros = new URLSearchParams(window.location.search);

const categoria = parametros.get("categoria");

const contenedor = document.getElementById("lista-productos");

const titulo = document.getElementById("titulo-categoria");


function formatearPrecio(precio) {
    return "$" + precio.toLocaleString("es-CL");
}


function mostrarProductos() {

    let productosFiltrados = productos;

    if (categoria) {
        productosFiltrados = productos.filter(
            producto => producto.categoria === categoria
        );
    }

    if (categoria === "panaderia") {
        titulo.textContent = "Panadería";
    } else if (categoria === "pasteleria") {
        titulo.textContent = "Pastelería";
    } else if (categoria === "facturas") {
        titulo.textContent = "Facturas";
    } else {
        titulo.textContent = "Nuestros productos";
    }

    contenedor.innerHTML = "";

    productosFiltrados.forEach(producto => {

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
mostrarProductos();