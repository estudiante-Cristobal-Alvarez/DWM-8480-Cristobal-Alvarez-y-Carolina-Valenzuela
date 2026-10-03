Cristóbal Álvarez
Carolina Valenzuela
Descripción del proyecto
Este repositorio contiene el desarrollo del proyecto Dulce Hogar, realizado para la asignatura Desarrollo Movil y Web.

Dulce Hogar corresponde a una propuesta de sitio web orientado a una panadería y pastelería, en el cual los usuarios pueden navegar por diferentes categorías de productos, consultar los productos disponibles y acceder al detalle de cada uno.

En la etapa actual se encuentra implementado el Frontend del proyecto, desarrollado mediante HTML, CSS, Bootstrap, JavaScript y con implementación de imágenes.

Frontend
El frontend de Dulce Hogar fue desarrollado considerando una estructura responsiva y una navegación sencilla entre las distintas secciones del sitio.

Actualmente se encuentran implementadas las siguientes páginas:

Página principal.
Catálogo de Panadería.
Catálogo de Pastelería.
Catálogo de Facturas.
Detalle de Productos.
Página de Contacto.
El frontend se encuentra disponible dentro de la carpeta:

Frontend Dulce Hogar/

Además, se incluye una copia preparada para su publicación mediante GitHub Pages dentro de:

docs/

Características implementadas
El frontend cuenta actualmente con las siguientes características:

Diseño responsiva mediante Bootstrap.
Uso de HTML para la estructura de las páginas.
Uso de CSS para la personalización visual del sitio.
Uso de JavaScript para la interacción y carga de productos.
Separación de productos por categorías.
Visualización de imágenes, nombres y precios de los productos.
Página individual para visualizar los detalles de cada producto.
Navegación entre las diferentes secciones del sitio.
Navegación mediante parámetros en la URL utilizando JavaScript.
Retorno desde el detalle de un producto hacia su catálogo correspondiente.
Página de contacto.
Barra de navegación disponible en las diferentes secciones.
Footer con información general de Dulce Hogar.
Uso de una paleta de colores definidas para mantener una identidad visual consistente. Elaboración propia de la paleta de colores.
Interacción mediante URL
Para la visualización de los productos se utiliza JavaScript junto con parámetros enviados mediante la URL.

Por ejemplo:

producto.html?id=hamburguesa-brioche

JavaScript obtiene el identificador enviado en la URL y utiliza este valor para mostrar la información correspondiente al producto seleccionado.

Esto permite reutilizar la página producto.html para mostrar diferentes productos sin necesidad de crear una página HTML independiente para cada uno.

Mapa del sitio
La navegación principal del frontend se encuentra organizada de la siguiente manera:

Inicio
│
├── Panadería
│   ├─ Catálogo de productos
│   └─ Detalle del producto -> Volver al catálogo de Panadería
│        
│
├── Pastelería
│   ├─ Catálogo de productos
│   └─ Detalle del producto -> Volver al catálogo de Pastelería
│        
│
├── Facturas
│   ├── Catálogo de productos
│   └── Detalle del producto -> Volver al catálogo de Facturas
|
└── Contacto


Frontend Dulce Hogar/
│
├── css/ -> Archivos de estilos
│    
│
├── img/ -> Imágenes utilizadas por el sitio
│    
│
├── js/ -> Archivos JavaScript
│    
│
├── index.html
├── panaderia.html
├── pasteleria.html
├── bolleria.html
├── producto.html
└── contacto.html


Para la publicación mediante GitHub Pages se utiliza la carpeta:

docs/
│
├── css/
├── img/
├── js/
├── index.html
├── panaderia.html
├── pasteleria.html
├── bolleria.html
├── producto.html
└── contacto.html

