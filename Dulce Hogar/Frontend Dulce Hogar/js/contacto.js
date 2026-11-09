const formulario =
    document.getElementById("formulario-contacto");

const respuesta =
    document.getElementById("respuesta");


formulario.addEventListener(
    "submit",
    function (evento) {

        evento.preventDefault();

        const nombre =
            document.getElementById("nombre").value;

        const tipo =
            document.getElementById("tipo").value;

        respuesta.innerHTML = `
            <div class="alert alert-success">

                Gracias, ${nombre}.

                Tu ${tipo} ha sido registrada
                correctamente.

            </div>
        `;

        formulario.reset();
    }
);