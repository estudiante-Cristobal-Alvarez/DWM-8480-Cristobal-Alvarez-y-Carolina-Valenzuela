// Creación de elementos en html con JavaScript

// Limpiar contenido del body
document.body.innerHTML = "";

// Creación de título
let titulo = document.createElement("h2");

titulo.innerText = "Ejemplo de creación de elementos con JavaScript";
document.body.appendChild(titulo);

// Crear cuadro de texto
let texto = document.createElement("input");

texto.setAttribute("type", "text");
texto.setAttribute("value", "bienvenid@");
texto.setAttribute("name", "txtMensaje");
texto.setAttribute("id", "txtMensaje");

document.body.appendChild(texto);

document.body.appendChild(document.createElement("br"));
document.body.appendChild(document.createElement("br"));

// Simulación de respuesta de una API
const responseAPI = {
    "status": 200,
    "message": "Productos Obtenidos",
    "data": [
        {
            "id": "1", 
            "nombre": "Manzana",
            "precio": 1500,
            "unidad": "Kg"
        },

        {
            "id": "2",
            "nombre": "Pera",
            "precio": 1200,
            "unidad": "Kg"
        },

        {
            "id": "3",
            "nombre": "Bebestibles",
            "precio": 3900,
            "unidad": "Pack de seis"
        },

        {
            "id": "4",
            "nombre": "Zanahorias",
            "precio": 900,
            "unidad": "Kg"
        }
    ]
};

// Creación del select
let seleccion = document.createElement("select");
seleccion.setAttribute("name", "seleccion");
seleccion.setAttribute("id", "seleccion");

// Opción inicial
let opcionInicial = document.createElement("option");
opcionInicial.setAttribute("value", "");
opcionInicial.innerText = "Seleccione un producto"; 
seleccion.appendChild(opcionInicial);

// Recorrer productos de la API

responseAPI.data.forEach((producto) => {

    let optionAux = document.createElement("option");

    // El value guarda el ID
    optionAux.setAttribute("value", producto.id);

    // Mostramos nombre y precio
    optionAux.innerText = producto.nombre; 

    // Agregamos el option al select
    seleccion.appendChild(optionAux);
});


// Agregar select al documento
document.body.appendChild(seleccion);
document.body.appendChild(document.createElement("br"));
document.body.appendChild(document.createElement("br"));

// Creación del botón
let boton = document.createElement("button");
boton.innerText = "Mostrar selección";
document.body.appendChild(boton);

// Párrafo para mostrar resultado
let resultado = document.createElement("p");
document.body.appendChild(resultado);

// Evento del botón
boton.addEventListener("click",() => 
    {
        // Obtener texto escrito
        let mensaje = texto.value;

        // Obtener ID seleccionado
        let idSeleccionado = seleccion.value;

        // Verificar que se haya seleccionado algo
        if (idSeleccionado === "") {
            resultado.innerText = "Debe seleccionar un producto.";
        } else {

            // Buscar el producto según su ID
            let productoSeleccionado = responseAPI.data.find((producto) =>
                        producto.id === idSeleccionado);

            // Mostrar los datos
            resultado.innerText = "Texto: " + mensaje +
                " | Producto: " +
                productoSeleccionado.nombre +
                " | Precio: $" +
                productoSeleccionado.precio +
                " | Unidad: " +
                productoSeleccionado.unidad +
                " | ID: " +
                productoSeleccionado.id;
        }
    }
);

// Orientación a objectos con JavaScript


// Crear un objeto producto

const producto = {
    id: "1",
    nombre: "Manzana",
    precio: 1500,
    unidad: "Kg"
};

console.log("Producto original:");
console.log(producto);

// Acceder a propiedades
console.log(producto.nombre);
console.log(producto.precio);

// También podemos utilizar []
console.log(producto["nombre"]);

// Agregar una nueva propiedad
producto.stock = 20;
console.log("Producto con stock:");
console.log(producto);

// Modificar una propiedad
producto.precio = 1600;

console.log("Producto con nuevo precio:");
console.log(producto);

//  Eliminar una propiedad
delete producto.stock;
console.log( "Producto después de eliminar stock:");
console.log(producto);

// Spread Operator
const productoActualizado = {
    ...producto,
    oferta: true,
    descuento: 10
};

console.log("Producto actualizado:");
console.log(productoActualizado);

// Crear otro objeto
const proveedor = {
    nombreProveedor: "Frutas del Sur",
    ciudad: "Santiago"
};

console.log("Proveedor:");
console.log(proveedor);

// Fusionar objetos con Object.assign

const fusion = Object.assign(
    {}, 
    productoActualizado,
    proveedor
);

console.log("Fusión con Object.assign:");
console.log(fusion);

// Fusionar utilizando Spread
const fusionSpread = {
    ...productoActualizado,
    ...proveedor
};

console.log("Fusión utilizando Spread:");
console.log(fusionSpread);

// Composición
const composicion = {
    productoActualizado,
    proveedor
};

console.log("Composición:");
console.log(composicion);

// Acceder a objetos internos
console.log(composicion.productoActualizado.nombre);
console.log(composicion.proveedor.nombreProveedor);

// for...in
console.log("Recorrido con for...in:");

for (let propiedad in productoActualizado) {
    console.log(propiedad, productoActualizado[propiedad]);
}

// Object.keys()
console.log("Claves:");
Object.keys(productoActualizado).forEach((clave) => {
    console.log(clave);
});

// Object.values()
console.log("Valores:");
Object.values(productoActualizado).forEach((valor) => {
    console.log(valor);
});

// Object.entries()

console.log("Claves y valores:");
Object.entries(productoActualizado).forEach(([clave, valor]) => {
        console.log(`Clave: ${clave}, Valor: ${valor}`);
    }
);

// Recorrer objetos dentro de objetos
console.log("Recorrido de la composición:");
Object.entries(composicion).forEach(([nombreObjeto, objetoInterno]) => {
        console.log("Objeto:",nombreObjeto);
        Object.entries(objetoInterno).forEach(([clave, valor]) => {
                console.log(`${clave}: ${valor}`);
            }
        );
    }
);