let texto = document.createElement("input");
texto.setAttribute("type","text");
texto.setAttribute("value", "hola");
document.body.innerHTML = "";
document.body.appendChild(texto);

const responseAPI = {
    "status": 200,
    "message": "Productos Obtenidos",
    "data": [{"id":"1","nombre":"Martillo"},{"id":"2","nombre":"Tijera"}]
};

let cmbComuna = document.createElement("select");
cmbComuna.setAttribute("name","cmbComuna");
responseAPI.data.forEach((com) => {
  let optionAux = document.createElement("option");
  optionAux.setAttribute("value", com.id);
  optionAux.innerText = com.nombre;
  cmbComuna.appendChild(optionAux);
});
document.body.appendChild(cmbComuna);

