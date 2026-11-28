// Obtener los datos de la sesión actual
function obtenerSesion() {

    const token = sessionStorage.getItem("dulceHogarToken");

    const usuarioGuardado = sessionStorage.getItem("dulceHogarUsuario");

    // Si no existe token o usuario, no hay sesión
    if (!token || !usuarioGuardado) {
        return null;
    }

    try {

        // Obtener información del token JWT
        const partes = token.split(".");

        if (partes.length !== 3) {
            cerrarSesion(false);
            return null;
        }

        // Decodificar el contenido del token
        const base64 = partes[1]
            .replace(/-/g, "+")
            .replace(/_/g, "/");

        const payload = JSON.parse(atob(base64));

        // Obtener la fecha actual en segundos
        const ahora = Math.floor(Date.now() / 1000);

        // Comprobar que el token tenga una expiración válida
        if (
            typeof payload.exp !== "number" ||
            payload.exp <= ahora
        ) {

            cerrarSesion(false);
            return null;

        }

        // Recuperar los datos del usuario
        const usuario = JSON.parse(usuarioGuardado);

        if (!usuario || !usuario.nombre) {
            cerrarSesion(false);
            return null;
        }

        return {
            token: token,
            usuario: usuario
        };

    } catch (error) {

        console.error("No se pudo recuperar la sesión:", error);

        cerrarSesion(false);

        return null;

    }

}

// Cerrar sesión

function cerrarSesion(mostrarMensaje = true) {

    // Eliminar los datos de autenticación
    sessionStorage.removeItem("dulceHogarToken");

    sessionStorage.removeItem("dulceHogarUsuario");

    // Actualizar el menú si ya está disponible
    actualizarMenuUsuario();

    if (mostrarMensaje) {
        alert("Has cerrado sesión correctamente.");
    }

}


// ACTUALIZAR MENÚ DE NAVEGACIÓN

function actualizarMenuUsuario() {

    const botonLogin = document.getElementById("openLoginBtn");

    if (!botonLogin) {
        return;
    }

    const sesion = obtenerSesion();

    // Buscar el menú de usuario, si ya fue creado
    let menuUsuario = document.getElementById("menuUsuario");

    // Si no hay sesión, mostrar el botón de login
    if (!sesion) {

        botonLogin.style.display = "";

        if (menuUsuario) {
            menuUsuario.remove();
        }

        return;
    }

    // Si hay sesión, ocultar el botón de login
    botonLogin.style.display = "none";

    // Evitar crear el menú dos veces
    if (menuUsuario) {
        menuUsuario.remove();
    }

    // Crear el contenedor del menú
    menuUsuario = document.createElement("div");

    menuUsuario.id = "menuUsuario";
    menuUsuario.className = "dropdown";

    // Crear el botón del usuario
    const botonUsuario = document.createElement("button");

    botonUsuario.type = "button";

    botonUsuario.className = "nav-login-btn dropdown-toggle";

    botonUsuario.setAttribute("data-bs-toggle", "dropdown");

    botonUsuario.setAttribute("aria-expanded", "false");

    botonUsuario.textContent = `Hola, ${sesion.usuario.nombre}`;

    // Crear las opciones del menú
    const listaOpciones = document.createElement("ul");

    listaOpciones.className = "dropdown-menu dropdown-menu-end";

    // Crear la opción de cerrar sesión
    const opcionCerrar = document.createElement("li");

    const botonCerrar = document.createElement("button");

    botonCerrar.type = "button";

    botonCerrar.className = "dropdown-item";

    botonCerrar.textContent = "Cerrar sesión";

    // Asociar el evento de cierre de sesión
    botonCerrar.addEventListener("click", () => {

        cerrarSesion();

    });

    // Incorporar los elementos
    opcionCerrar.appendChild(botonCerrar);

    listaOpciones.appendChild(opcionCerrar);

    menuUsuario.appendChild(botonUsuario);

    menuUsuario.appendChild(listaOpciones);

    // Insertar el menú junto al botón original
    botonLogin.insertAdjacentElement("afterend", menuUsuario);

}


// Iniciar sesión

document.addEventListener("DOMContentLoaded", () => {

    actualizarMenuUsuario();

});

// Permitir que auth.js actualice el menú después del login
window.dulceHogarActualizarSesion = actualizarMenuUsuario;