// Dirección del servicio de autenticación
const AUTH_API_URL = "http://127.0.0.1:8001";

document.addEventListener("DOMContentLoaded", () => {

    // Elementos del formulario de login
    const loginForm = document.getElementById("loginForm");
    const loginModal = document.getElementById("loginModal");
    const loginEmail = document.getElementById("loginEmail");
    const loginPassword = document.getElementById("loginPassword");
    const openLoginBtn = document.getElementById("openLoginBtn");

    // Elementos del formulario de registro
    const loginSection = document.getElementById("loginSection");
    const registerSection = document.getElementById("registerSection");

    const showRegisterBtn = document.getElementById("showRegisterBtn");
    const showLoginBtn = document.getElementById("showLoginBtn");

    const registerForm = document.getElementById("registerForm");

    // Comprobar que existe el formulario de login
    if (!loginForm) {
        return;
    }


    // ==========================================
    // CAMBIAR ENTRE LOGIN Y REGISTRO
    // ==========================================

    // Mostrar el formulario de registro
    if (showRegisterBtn && loginSection && registerSection) {

        showRegisterBtn.addEventListener("click", (event) => {

            event.preventDefault();

            // Ocultar login
            loginSection.style.display = "none";

            // Mostrar registro
            registerSection.style.display = "block";

        });

    }


    // Volver al formulario de login
    if (showLoginBtn && loginSection && registerSection) {

        showLoginBtn.addEventListener("click", (event) => {

            event.preventDefault();

            // Ocultar registro
            registerSection.style.display = "none";

            // Mostrar login
            loginSection.style.display = "block";

        });

    }


    // ==========================================
    // INICIO DE SESIÓN
    // ==========================================

    loginForm.addEventListener("submit", async (event) => {

        // Evitar que se recargue la página
        event.preventDefault();

        // Obtener los datos escritos por el usuario
        const correo = loginEmail.value.trim();
        const password = loginPassword.value;

        // Validar que los campos no estén vacíos
        if (!correo || !password) {

            alert("Por favor, completa todos los campos.");

            return;
        }

        try {

            // Enviar las credenciales a FastAPI
            const respuesta = await fetch(
                `${AUTH_API_URL}/login`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        correo: correo,
                        password: password
                    })
                }
            );

            // Convertir la respuesta a JSON
            const datos = await respuesta.json();

            // Comprobar si ocurrió algún error
            if (!respuesta.ok) {

                if (respuesta.status === 401) {

                    alert("Correo o contraseña incorrectos.");

                }
                else if (respuesta.status === 403) {

                    alert("Tu cuenta está desactivada.");

                }
                else if (respuesta.status === 503) {

                    alert("El servicio de autenticación no está disponible.");

                }
                else {

                    alert("No se pudo iniciar sesión.");

                }

                return;
            }

            // Guardar el token JWT
            sessionStorage.setItem(
                "dulceHogarToken",
                datos.access_token
            );

            // Guardar información del usuario
            sessionStorage.setItem(
                "dulceHogarUsuario",
                JSON.stringify(datos.usuario)
            );

            // Mostrar mensaje de bienvenida
            alert(`¡Bienvenida/o, ${datos.usuario.nombre}!`);

            // Limpiar contraseña
            loginPassword.value = "";

            // Cerrar ventana emergente
            loginModal.classList.remove("active");

            loginModal.setAttribute(
                "aria-hidden",
                "true"
            );

            // Actualizar botón del menú
            if (openLoginBtn) {

                openLoginBtn.textContent =
                    `Hola, ${datos.usuario.nombre}`;

            }

        } catch (error) {

            console.error(
                "Error al conectar con Auth Service:",
                error
            );

            alert(
                "No se pudo conectar con el servidor. " +
                "Comprueba que Auth Service esté funcionando."
            );

        }

    });


    // ==========================================
    // REGISTRO DE USUARIOS
    // ==========================================

    if (registerForm) {

        registerForm.addEventListener("submit", async (event) => {

            // Evitar que se recargue la página
            event.preventDefault();

            // Obtener los datos del formulario
            const nombre = document.getElementById(
                "registerName"
            ).value.trim();

            const correo = document.getElementById(
                "registerEmail"
            ).value.trim();

            const password = document.getElementById(
                "registerPassword"
            ).value;

            const confirmarPassword = document.getElementById(
                "registerConfirmPassword"
            ).value;

            // Comprobar que las contraseñas coincidan
            if (password !== confirmarPassword) {

                alert("Las contraseñas no coinciden.");

                return;
            }

            try {

                // Enviar los datos a FastAPI
                const respuesta = await fetch(
                    `${AUTH_API_URL}/register`,
                    {
                        method: "POST",

                        headers: {
                            "Content-Type": "application/json"
                        },

                        body: JSON.stringify({
                            nombre: nombre,
                            correo: correo,
                            password: password
                        })
                    }
                );

                // Leer la respuesta del backend
                const datos = await respuesta.json();

                // Comprobar si ocurrió algún error
                if (!respuesta.ok) {

                    if (respuesta.status === 409) {

                        alert(
                            "Este correo electrónico ya está registrado."
                        );

                    }
                    else if (respuesta.status === 422) {

                        alert(
                            "Revisa los datos ingresados."
                        );

                    }
                    else {

                        alert(
                            "No se pudo completar el registro."
                        );

                    }

                    return;
                }

                // Registro exitoso
                alert(
                    "¡Cuenta creada correctamente! " +
                    "Ahora puedes iniciar sesión."
                );

                // Limpiar el formulario de registro
                registerForm.reset();

                // Ocultar formulario de registro
                registerSection.style.display = "none";

                // Mostrar formulario de login
                loginSection.style.display = "block";

                // Completar automáticamente el correo
                loginEmail.value = correo;

            } catch (error) {

                console.error(
                    "Error al registrar usuario:",
                    error
                );

                alert(
                    "No se pudo conectar con el servidor de autenticación."
                );

            }

        });

    }

});