// Creación de elementos en html con javascript



// Limpiar contenido
document.body.innerHTML = "";

// Creación de titulo
let titulo = document.createElement("h2");
titulo.innerText = "Ejemplo de creación de elementos con JavaScript";

document.body.appendChild(titulo);



// Crea cuadro de texto
let texto = document.createElement("input");
texto.setAttribute("type", "text");
texto.setAttribute("value", "bienvenid@");
texto.setAttribute("name", "txtMensaje");
texto.setAttribute("price", "textNumero");
texto.setAttribute("id", "txtMensaje");

// Se agrega el input al body
document.body.appendChild(texto);

// Agregamos un salto de línea
document.body.appendChild(document.createElement("br"));
document.body.appendChild(document.createElement("br"));


// ------------------------------------------
// 3. Simulación de respuesta de una API
// ------------------------------------------

const responseAPI = {
    "status": 200,
    "message": "Productos Obtenidos",
    "data": [
        {
            "id": "1",
            "nombre": "Manzana",
            "Precio": "$1500 el Kg"
        },
        {
            "id": "2",
            "nombre": "Pera",
            "precio": "$1200 el Kg"
        },
        {
            "id": "3",
            "nombre": "Bebestibles",
            "precio": "$3900 el pack de seis"
        },  
        {
            "id": "4",
            "nombre": "Zanahorias",
            "precio": "$900 el Kg"
        }
    ]
};


// ------------------------------------------
// 4. Crear un select
// ------------------------------------------

let cmbComuna = document.createElement("select");

cmbComuna.setAttribute("name", "cmbComuna");
cmbComuna.setAttribute("id", "cmbComuna");


// ------------------------------------------
// 5. Crear opción inicial
// ------------------------------------------

let opcionInicial = document.createElement("option");

opcionInicial.setAttribute("value", "");
opcionInicial.innerText = "Seleccione un producto";

cmbComuna.appendChild(opcionInicial);


// ------------------------------------------
// 6. Recorrer los datos provenientes de API
// ------------------------------------------

responseAPI.data.forEach((com) => {

    // Creamos un option por cada producto
    let optionAux = document.createElement("option");

    // El value contiene el ID del producto
    optionAux.setAttribute("value", com.id);

    // Lo que ve el usuario es el nombre
    optionAux.innerText = com.nombre;

    // Agregamos la opción al select
    cmbComuna.appendChild(optionAux);
});


// Agregamos el select al documento
document.body.appendChild(cmbComuna);


// Salto de línea
document.body.appendChild(document.createElement("br"));
document.body.appendChild(document.createElement("br"));


// ------------------------------------------
// 7. Crear un botón
// ------------------------------------------

let boton = document.createElement("button");

boton.innerText = "Mostrar selección";

document.body.appendChild(boton);


// ------------------------------------------
// 8. Crear un párrafo para mostrar resultados
// ------------------------------------------

let resultado = document.createElement("p");

document.body.appendChild(resultado);


// ------------------------------------------
// 9. Evento del botón
// ------------------------------------------

boton.addEventListener("click", () => {

    // Obtener texto escrito
    let mensaje = texto.value;

    // Obtener ID seleccionado
    let idSeleccionado = cmbComuna.value;

    // Obtener texto de la opción seleccionada
    let nombreSeleccionado =
        cmbComuna.options[cmbComuna.selectedIndex].text;


    if (idSeleccionado === "") {

        resultado.innerText =
            "Debe seleccionar un producto.";

    } else {

        resultado.innerText =
            "Texto: " + mensaje +
            " | Producto: " + nombreSeleccionado +
            " | ID: " + idSeleccionado;
    }

});

