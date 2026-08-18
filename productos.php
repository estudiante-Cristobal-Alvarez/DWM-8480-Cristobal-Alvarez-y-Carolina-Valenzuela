<!DOCTYPE html>
<html lang="es">
    <head>
        <title>Pagina productos</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css" rel="stylesheet">
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js"></script>
    </head>
    <body>
        <!-- Navbar -->
        <nav class="navbar navbar-expand-sm navbar-dark" style="background-color:rgb(9,96,174);">
            <div class="container-fluid">
                <a class="navbar-brand" href="index.php">
                    <img src="img/Company.png" alt="Empresa" width="60">
                </a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#collapsibleNavbar">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="collapsibleNavbar">
                    <ul class="navbar-nav">
                        <li class="nav-item dropdown">
                            <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">Empresa</a>
                            <ul class="dropdown-menu">
                                <li><a class="dropdown-item" href="empresa.php">Quienes somos</a></li>
                                <li><a class="dropdown-item" href="contacto.php">Nuestro equipo</a></li>
                                <li><a class="dropdown-item" href="#" data-bs-toggle="modal" data-bs-target="#modalMision">Misión</a></li>
                            </ul>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="productos.php">Productos</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="servicios.php">Servicios</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="contacto.php">Contacto</a>
                        </li>
                    </ul>
                </div>
                <button type="button" class="btn btn-dark" data-bs-toggle="modal" data-bs-target="#myModal">Acceder</button>   
            </div>
        </nav>

        <!-- Container -->
        <div class="container-fluid" style="background-color:#8fbfec;">        
        <strong>Conoce nuestros productos</strong><br>
            <!-- Carousel -->
            <div id="demo" class="carousel slide" data-bs-ride="carousel">

                <!-- Indicators/dots -->
                <div class="carousel-indicators">
                    <button type="button" data-bs-target="#demo" data-bs-slide-to="0" class="active"></button>
                    <button type="button" data-bs-target="#demo" data-bs-slide-to="1"></button>
                    <button type="button" data-bs-target="#demo" data-bs-slide-to="2"></button>
                </div>

                <!-- The slideshow/carousel -->
                <div class="carousel-inner">

                    <!-- Primera imagen -->
                    <div class="carousel-item active">
                        <div class="d-flex justify-content-center align-items-center">
                            <img src="img/Bebestibles.png" alt="Bebestibles" class="d-block" width="300">
                        </div>
                    </div>

                    <!-- Segunda imagen -->
                    <div class="carousel-item">
                        <div class="d-flex justify-content-center align-items-center">
                            <img src="img/Frutas.png" alt="Frutas" class="d-block" width="300">
                        </div>
                    </div>

                    <!-- Tercera imagen -->
                    <div class="carousel-item">
                        <div class="d-flex justify-content-center align-items-center">
                            <img src="img/Verduras.png" alt="Verduras" class="d-block" width="300">
                        </div>
                    </div>

                </div>

                <!-- Left and right controls/icons -->
                <button class="carousel-control-prev" type="button" data-bs-target="#demo" data-bs-slide="prev">
                    <span class="carousel-control-prev-icon"></span>
                </button>
                <button class="carousel-control-next" type="button" data-bs-target="#demo" data-bs-slide="next">
                    <span class="carousel-control-next-icon"></span>
                </button>
            </div>  
        </div>
        <!-- Footer -->
        <div class="container-fluid" style="background-color:rgb(9,96,174);">
            <div class="row">
                <div class="col-4"></div>
                <div class="col-4">
                    <strong class="text-white">Miempresa@2026.cl</strong></div>
                <div class="col-4"></div>
                </div>
        </div>

        <!-- Modal -->
        <div class="modal fade" id="myModal">
            <div class="modal-dialog">
                <div class="modal-content">

                <!-- Modal Header -->
                <div class="modal-header">
                    <h4 class="modal-title">Acceder</h4>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <!-- Modal body -->
                <div class="modal-body">
                    hola :)
                    <form action="empresa.php">
                        <div class="mb-3 mt-3">
                            <label for="email" class="form-label">Email:</label>
                            <input type="email" class="form-control" id="email" placeholder="Enter email" name="email">
                        </div>
                        <div class="mb-3">
                            <label for="pwd" class="form-label">Password:</label>
                            <input type="password" class="form-control" id="pwd" placeholder="Enter password" name="pswd">
                        </div>
                        <div class="form-check mb-3">
                            <label class="form-check-label">
                            <input class="form-check-input" type="checkbox" name="remember"> Remember me
                            </label>
                        </div>
                        <button type="submit" class="btn btn-primary">Submit</button>
                    </form>
                </div>

                <!-- Modal footer -->
                <div class="modal-footer">
                    <button type="button" class="btn btn-danger" data-bs-dismiss="modal">Cerrar</button>
                </div>

                </div>
            </div>
        </div>

         
         <!-- MODAL MISIÓN -->
   

        <div class="modal fade" id="modalMision">
            <div class="modal-dialog">
                <div class="modal-content">
                    <!-- Encabezado del modal -->
                    <div class="modal-header">
                        <h4 class="modal-title">
                            Nuestra Misión
                        </h4><button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>


                    <!-- Contenido de la misión -->
                    <div class="modal-body">
                        <p>
                            Contribuir a la nutrición, salud y bienestar
                            de las personas, poniendo a su disposición
                            productos de la más alta calidad.
                        </p>
                    </div>

                    <!-- Botón cerrar -->
                    <div class="modal-footer">
                        <button type="button" class="btn btn-primary" data-bs-dismiss="modal">Cerrar</button>
                    </div>
                </div>
            </div>
        </div>
    </body>
</html>