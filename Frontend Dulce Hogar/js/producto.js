const productos = [
    {
        "id": "hamburguesa-brioche",
        "nombre": "Hamburguesa Brioche",
        "categoria": "panaderia",
        "precio": 3690,
        "imagen": "img/panes/Pan Hamburguesa Brioche Granel 3690 x kg.png",
        "descripcion": "Hamburguesa Brioche, producto de panadería de Dulce Hogar."
    },
    {
        "id": "hogaza-multi-wholegrain",
        "nombre": "Hogaza Multi Wholegrain 700 g",
        "categoria": "panaderia",
        "precio": 4700,
        "imagen": "img/panes/Pan Hogaza Multi Wholegrain 700 g 4700 x kg.png",
        "descripcion": "Hogaza Multi Wholegrain 700 g, producto de panadería de Dulce Hogar."
    },
    {
        "id": "hoja",
        "nombre": "Hoja Granel",
        "categoria": "panaderia",
        "precio": 5490,
        "imagen": "img/panes/Pan Hoja Granel 5490 x kg.png",
        "descripcion": "Hoja Granel, producto de panadería de Dulce Hogar."
    },
    {
        "id": "hot-dog",
        "nombre": "Hot Dog Granel",
        "categoria": "panaderia",
        "precio": 3290,
        "imagen": "img/panes/Pan Hot Dog Granel 3290 x kg.png",
        "descripcion": "Hot Dog Granel, producto de panadería de Dulce Hogar."
    },
    {
        "id": "landbrot",
        "nombre": "Pan Landbrot 800 g",
        "categoria": "panaderia",
        "precio": 4363,
        "imagen": "img/panes/Pan Landbrot 800 g 4363 x kg.png",
        "descripcion": "Pan Landbrot 800 g, producto de panadería de Dulce Hogar."
    },
    {
        "id": "marraqueta-grande",
        "nombre": "Marraqueta Grande",
        "categoria": "panaderia",
        "precio": 2290,
        "imagen": "img/panes/Pan Marraqueta Grande 2290 x kg.jpg",
        "descripcion": "Marraqueta Grande, producto de panadería de Dulce Hogar."
    },
    {
        "id": "amasado",
        "nombre": "Amasado Granel",
        "categoria": "panaderia",
        "precio": 3290,
        "imagen": "img/panes/Pan Amasado Granel 3290 x kg.png",
        "descripcion": "Amasado Granel, producto de panadería de Dulce Hogar."
    },
    {
        "id": "baguetin-rustico",
        "nombre": "Baguetín Rústico Granel",
        "categoria": "panaderia",
        "precio": 3490,
        "imagen": "img/panes/Pan Baguetin Rustico Granel 3690 x kg.png",
        "descripcion": "Baguetín Rústico Granel, producto de panadería de Dulce Hogar."
    },
    {
        "id": "baguette-rustico",
        "nombre": "Baguette Rústico Tradicional",
        "categoria": "panaderia",
        "precio": 4967,
        "imagen": "img/panes/Pan Baguette Rustico Tradicional 1 un. 4967 x kg.png",
        "descripcion": "Baguette Rústico Tradicional, producto de panadería de Dulce Hogar."
    },
    {
        "id": "bocado-dama",
        "nombre": "Bocado de Dama Granel",
        "categoria": "panaderia",
        "precio": 4490,
        "imagen": "img/panes/Pan Bocado de Dama Granel 4490 x kg.png",
        "descripcion": "Bocado de Dama Granel, producto de panadería de Dulce Hogar."
    },
    {
        "id": "campo-cinco-granos",
        "nombre": "Campo 5 Granos Granel",
        "categoria": "panaderia",
        "precio": 5978,
        "imagen": "img/panes/Pan Campo 5 Granos Granel 5978 x kg.png",
        "descripcion": "Campo 5 Granos Granel, producto de panadería de Dulce Hogar."
    },
    {
        "id": "ciabatta-famiglia",
        "nombre": "Ciabatta Famiglia Artesanal",
        "categoria": "panaderia",
        "precio": 3490,
        "imagen": "img/panes/Pan Ciabatta Famiglia Artesanal 3490 x kg.png",
        "descripcion": "Ciabatta Famiglia Artesanal, producto de panadería de Dulce Hogar."
    },
    {
        "id": "ciabatta",
        "nombre": "Ciabatta Granel",
        "categoria": "panaderia",
        "precio": 3490,
        "imagen": "img/panes/Pan Ciabatta Granel 3490 x kg.jpg",
        "descripcion": "Ciabatta Granel, producto de panadería de Dulce Hogar."
    },
    {
        "id": "ciabatta-integral",
        "nombre": "Ciabatta Integral Granel",
        "categoria": "panaderia",
        "precio": 3490,
        "imagen": "img/panes/Pan Ciabatta Integral Granel 3490 x kg.png",
        "descripcion": "Ciabatta Integral Granel, producto de panadería de Dulce Hogar."
    },
    {
        "id": "coliza",
        "nombre": "Coliza Granel",
        "categoria": "panaderia",
        "precio": 3490,
        "imagen": "img/panes/Pan Coliza Granel 3490 x kg.png",
        "descripcion": "Coliza Granel, producto de panadería de Dulce Hogar."
    },
    {
        "id": "coliza-peruana",
        "nombre": "Coliza Peruana Granel",
        "categoria": "panaderia",
        "precio": 3690,
        "imagen": "img/panes/Pan Coliza Peruana Granel 3690 x kg.png",
        "descripcion": "Coliza Peruana Granel, producto de panadería de Dulce Hogar."
    },
    {
        "id": "pan-hamburguesa",
        "nombre": "Hamburguesa Granel",
        "categoria": "panaderia",
        "precio": 3290,
        "imagen": "img/panes/Pan de Hamburguesa Granel 3290 x kg.png",
        "descripcion": "Hamburguesa Granel, producto de panadería de Dulce Hogar."
    },
    {
        "id": "hallulla-delgada",
        "nombre": "Hallulla Delgada Granel",
        "categoria": "panaderia",
        "precio": 2990,
        "imagen": "img/panes/Pan Hallulla Delgada Granel 2290 x kg.png",
        "descripcion": "Hallulla Delgada Granel, producto de panadería de Dulce Hogar."
    },
    {
        "id": "hallulla",
        "nombre": "Hallulla Granel",
        "categoria": "panaderia",
        "precio": 2190,
        "imagen": "img/panes/Pan Hallulla Granel 2190 x kg.png",
        "descripcion": "Hallulla Granel, producto de panadería de Dulce Hogar."
    },
    {
        "id": "hallulla-integral",
        "nombre": "Hallulla Integral Linaza Granel",
        "categoria": "panaderia",
        "precio": 2990,
        "imagen": "img/panes/Pan Hallulla Integral Linaza Granel 2990 x kg.png",
        "descripcion": "Hallulla Integral Linaza Granel, producto de panadería de Dulce Hogar."
    },
    {
        "id": "rositas",
        "nombre": "Rositas Granel",
        "categoria": "panaderia",
        "precio": 2990,
        "imagen": "img/panes/Pan Rositas Granel 2990 x kg.png",
        "descripcion": "Rositas Granel, producto de panadería de Dulce Hogar."
    },
    {
        "id": "rustikal-brot",
        "nombre": "Rustikal Brot 850 g",
        "categoria": "panaderia",
        "precio": 4341,
        "imagen": "img/panes/Pan Rustikal Brot 850 g 4341 x kg.png",
        "descripcion": "Rustikal Brot 850 g, producto de panadería de Dulce Hogar."
    },
    {
        "id": "toscano",
        "nombre": "Toscano Granel",
        "categoria": "panaderia",
        "precio": 3490,
        "imagen": "img/panes/Pan Toscano Granel 3490 x kg.png",
        "descripcion": "Toscano Granel, producto de panadería de Dulce Hogar."
    },
    {
        "id": "marraqueta-wholegrain",
        "nombre": "Marraqueta Wholegrain Granel",
        "categoria": "panaderia",
        "precio": 3290,
        "imagen": "img/panes/Pan Marraqueta Wholegrain Granel 3290 x kg.png",
        "descripcion": "Marraqueta Wholegrain Granel, producto de panadería de Dulce Hogar."
    },
    {
        "id": "pita-blanco",
        "nombre": "Pita Blanco Granel",
        "categoria": "panaderia",
        "precio": 3490,
        "imagen": "img/panes/Pan Pita Blanco Granel 3490 x kg.png",
        "descripcion": "Pita Blanco Granel, producto de panadería de Dulce Hogar."
    },
    {
        "id": "pita-integral",
        "nombre": "Pita Integral Chía Linaza Granel",
        "categoria": "panaderia",
        "precio": 3490,
        "imagen": "img/panes/Pan Pita Integral Chia Linaza Granel 3490 x kg.png",
        "descripcion": "Pita Integral Chía Linaza Granel, producto de panadería de Dulce Hogar."
    },
    {
        "id": "torta-selva-negra",
        "nombre": "Torta Selva Negra",
        "categoria": "pasteleria",
        "precio": 12990,
        "imagen": "img/pasteleria/selvanegra.png",
        "descripcion": "Torta Selva Negra, producto de pastelería de Dulce Hogar."
    },
    {
        "id": "pie-de-limon",
        "nombre": "Pie de Limón",
        "categoria": "pasteleria",
        "precio": 8990,
        "imagen": "img/pasteleria/piedelimon.png",
        "descripcion": "Pie de Limón, producto de pastelería de Dulce Hogar."
    },
    {
        "id": "torta-tres-leches",
        "nombre": "Torta Tres Leches",
        "categoria": "pasteleria",
        "precio": 11500,
        "imagen": "img/pasteleria/tresleches.png",
        "descripcion": "Torta Tres Leches, producto de pastelería de Dulce Hogar."
    },
    {
        "id": "tartaleta-frutas",
        "nombre": "Tartaleta de Frutas",
        "categoria": "pasteleria",
        "precio": 9500,
        "imagen": "img/pasteleria/tartaleta.png",
        "descripcion": "Tartaleta de Frutas, producto de pastelería de Dulce Hogar."
    },
    {
        "id": "brownie",
        "nombre": "Brownie",
        "categoria": "pasteleria",
        "precio": 1500,
        "imagen": "img/pasteleria/brownie.png",
        "descripcion": "Brownie, producto de pastelería de Dulce Hogar."
    },
    {
        "id": "tiramisu",
        "nombre": "Tiramisú",
        "categoria": "pasteleria",
        "precio": 9500,
        "imagen": "img/pasteleria/tiramisu.png",
        "descripcion": "Tiramisú, producto de pastelería de Dulce Hogar."
    },
    {
        "id": "cheescake-frambuesa",
        "nombre": "Cheesecake de frambuesa",
        "categoria": "pasteleria",
        "precio": 12000,
        "imagen": "img/pasteleria/cheesecakedeframbuesa.png",
        "descripcion": "Cheesecake de frambuesa, producto de pastelería de Dulce Hogar."
    },
    {
        "id": "rollos-canela",
        "nombre": "Rollos de canela",
        "categoria": "pasteleria",
        "precio": 5000,
        "imagen": "img/pasteleria/rollosdecanela.png",
        "descripcion": "Rollos de canela, producto de pastelería de Dulce Hogar."
    },
    {
        "id": "kuchen-manzana",
        "nombre": "Kuchen de manzana",
        "categoria": "pasteleria",
        "precio": 11500,
        "imagen": "img/pasteleria/kuchendemanzana.png",
        "descripcion": "Kuchen de manzana, producto de pastelería de Dulce Hogar."
    },
    {
        "id": "queque-vainilla",
        "nombre": "Queque de vainilla",
        "categoria": "pasteleria",
        "precio": 5500,
        "imagen": "img/pasteleria/quequedevainilla.png",
        "descripcion": "Queque de vainilla, producto de pastelería de Dulce Hogar."
    },
    {
        "id": "empolvados",
        "nombre": "Empolvados",
        "categoria": "pasteleria",
        "precio": 500,
        "imagen": "img/pasteleria/empolvados.png",
        "descripcion": "Empolvados, producto de pastelería de Dulce Hogar."
    },
    {
        "id": "chilenitos",
        "nombre": "Chilenitos",
        "categoria": "pasteleria",
        "precio": 500,
        "imagen": "img/pasteleria/chilenitos.png",
        "descripcion": "Chilenitos, producto de pastelería de Dulce Hogar."
    },
    {
        "id": "medialunas",
        "nombre": "Medialunas",
        "categoria": "facturas",
        "precio": 1200,
        "imagen": "img/bolleria/medialuna.png",
        "descripcion": "Medialunas, factura dulce de Dulce Hogar."
    },
    {
        "id": "canoncitos-dulce-de-leche",
        "nombre": "Cañoncitos con Manjar",
        "categoria": "facturas",
        "precio": 1500,
        "imagen": "img/bolleria/canoncito.png",
        "descripcion": "Cañoncitos con Manjar, factura dulce de Dulce Hogar."
    },
    {
        "id": "libritos",
        "nombre": "Libritos con Membrillo",
        "categoria": "facturas",
        "precio": 1300,
        "imagen": "img/bolleria/libritos.png",
        "descripcion": "Libritos con Membrillo, factura dulce de Dulce Hogar."
    },
    {
        "id": "pelotas-de-fraile",
        "nombre": "Bolas de Fraile (Suspiros de monja)",
        "categoria": "facturas",
        "precio": 1400,
        "imagen": "img/bolleria/pelotasdefraile.png",
        "descripcion": "Bolas de Fraile (Suspiros de monja), factura dulce de Dulce Hogar."
    },
    {
        "id": "sacramentos",
        "nombre": "Sacramentos",
        "categoria": "facturas",
        "precio": 1500,
        "imagen": "img/bolleria/sacramentos.png",
        "descripcion": "Sacramentos, factura dulce de Dulce Hogar."
    }
];


const parametros = new URLSearchParams(window.location.search);
const id = parametros.get("id");
const producto = productos.find(item => item.id === id);
const contenedor = document.getElementById("detalle-producto");

function formatearPrecio(precio) {
    return "$" + precio.toLocaleString("es-CL");
}

function rutaCatalogo(categoria) {
    if (categoria === "pasteleria") return "pasteleria.html";
    if (categoria === "facturas") return "bolleria.html";
    if (categoria === "panaderia") return "panaderia.html";
    return "producto.html?categoria=panaderia";
}

function nombreCategoria(categoria) {
    if (categoria === "pasteleria") return "Pastelería";
    if (categoria === "facturas") return "Facturas";
    return "Panadería";
}

if (producto) {
    contenedor.innerHTML = `
        <div class="row justify-content-center">
            <div class="col-md-8">
                <div class="card detalle">
                    <img
                        src="${producto.imagen}"
                        alt="${producto.nombre}"
                        class="producto-imagen-detalle"
                    >
                    <div class="card-body text-center">
                        <h2>${producto.nombre}</h2>
                        <p><strong>Categoría:</strong> ${nombreCategoria(producto.categoria)}</p>
                        <p>${producto.descripcion}</p>
                        <p class="precio">${formatearPrecio(producto.precio)}</p>
                        <a href="${rutaCatalogo(producto.categoria)}" class="btn boton-principal">
                            Volver al catálogo
                        </a>
                    </div>
                </div>
            </div>
        </div>
    `;
} else {
    contenedor.innerHTML = `
        <div class="alert alert-danger text-center">
            Producto no encontrado. <a href="index.html">Volver al inicio</a>
        </div>
    `;
}
