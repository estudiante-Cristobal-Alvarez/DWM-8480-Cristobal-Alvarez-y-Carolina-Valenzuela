workspace "Dulce Hogar" "Arquitectura del backend de Dulce Hogar" {

    !identifiers hierarchical

    model {
            cliente = person "Cliente" "Usuario que consulta productos y sus pedidos."
    
            sistema = softwareSystem "Dulce Hogar" "Backend de panaderia basado en microservicios." {
    
                
            gateway = container "Gateway GraphQL" "Consultas, agregacion de datos y autorizacion JWT." "FastAPI + Strawberry" {
    
                endpoint = component "Endpoint GraphQL" "Recibe consultas en /graphql." "Strawberry GraphQL"
    
                limites = component "Validador de consultas" "Controla profundidad maxima de 5 niveles y limite de 50 campos." "GraphQL Validation Rules"
        
                autenticacion = component "Autenticacion JWT" "Valida firma, vigencia e identidad del usuario." "PyJWT"
        
                autorizacion = component "Autorizacion de pedidos" "Comprueba que el pedido pertenezca al usuario autenticado." "Reglas de negocio"
        
                resolvers = component "Resolvers GraphQL" "Resuelve consultas de productos, pedidos y resumenes." "Python"
    
                integraciones = component "Clientes HTTP internos" "Consulta Orders, Inventory y Clients utilizando sus contratos internos." "HTTPX"

            }


            auth = container "Auth Service" "Registro, inicio de sesion y emision de JWT." "FastAPI + Argon2"

            inventory = container "Inventory Service" "Catalogo de productos y validacion de disponibilidad." "FastAPI + gRPC"

            orders = container "Orders Service" "Creacion y gestion de pedidos." "FastAPI"

            clients = container "Clients Service" "Gestion de datos de clientes." "FastAPI"

            payments = container "Payments Service" "Registro y actualizacion de pagos." "FastAPI"

            vault = container "Vault" "Almacenamiento de secretos para autenticacion." "HashiCorp Vault"

            dbAuth = container "Auth DB" "Usuarios y credenciales protegidas." "SQLite" {
                tags "Database"
            }

            dbInventory = container "Inventory DB" "Productos." "SQLite" {
                tags "Database"
            }

            dbOrders = container "Orders DB" "Pedidos y detalles." "SQLite" {
                tags "Database"
            }

            dbClients = container "Clients DB" "Datos de clientes." "SQLite" {
                tags "Database"
            }

            dbPayments = container "Payments DB" "Pagos." "SQLite" {
                tags "Database"
            }
        }

        cliente -> sistema "Consulta productos y pedidos mediante GraphQL"

        cliente -> sistema.gateway "Consulta productos y pedidos" "HTTP/GraphQL"
        cliente -> sistema.auth "Se registra e inicia sesion" "HTTP/JSON"
        
         // Relaciones internas del Gateway GraphQL
        sistema.gateway.endpoint -> sistema.gateway.limites "Valida la consulta"
        sistema.gateway.limites -> sistema.gateway.resolvers "Permite ejecutar la consulta valida"
        sistema.gateway.resolvers -> sistema.gateway.autenticacion "Verifica JWT cuando corresponde"
        sistema.gateway.autenticacion -> sistema.gateway.autorizacion "Entrega identidad autenticada"
        sistema.gateway.autorizacion -> sistema.gateway.integraciones "Consulta recursos autorizados"
        sistema.gateway.resolvers -> sistema.gateway.integraciones "Obtiene datos de productos y pedidos"

        // Comunicacion con los microservicios
        sistema.gateway.integraciones -> sistema.orders "Consulta pedidos" "HTTP/JSON"
        sistema.gateway.integraciones -> sistema.inventory "Consulta productos" "HTTP/JSON"
        sistema.gateway.integraciones -> sistema.clients "Verifica titular del pedido" "HTTP/JSON"

        sistema.orders -> sistema.clients "Valida clientes" "HTTP/JSON"
        sistema.orders -> sistema.inventory "Verifica disponibilidad" "gRPC"

        sistema.payments -> sistema.orders "Actualiza estado de pago" "HTTP/JSON"

        sistema.auth -> sistema.vault "Obtiene clave de firma JWT" "HTTP/Vault API"
        sistema.gateway -> sistema.vault "Obtiene clave para validar JWT" "HTTP/Vault API"

        sistema.auth -> sistema.dbAuth "Lee y escribe usuarios"
        sistema.inventory -> sistema.dbInventory "Lee productos"
        sistema.orders -> sistema.dbOrders "Lee y escribe pedidos"
        sistema.clients -> sistema.dbClients "Lee y escribe clientes"
        sistema.payments -> sistema.dbPayments "Lee y escribe pagos"
    }

    views {
        systemContext sistema "C1_Contexto" {
            title "C1 - Contexto del sistema Dulce Hogar"
            include *
            autoLayout lr
        }

        container sistema "C2_Contenedores" {
            title "C2 - Arquitectura de microservicios Dulce Hogar"
            include *
            autoLayout lr
        }
        
        component sistema.gateway "C3_Gateway" {
            title "C3 - Componentes del Gateway GraphQL"
            include *
            autoLayout lr
        }
        
        dynamic sistema "D_Registro_Pedido" {
            title "Flujo - Registro de pedido en Dulce Hogar"

            1: sistema.orders -> sistema.clients "Valida la existencia del cliente" "HTTP/JSON"
            2: sistema.orders -> sistema.inventory "Comprueba disponibilidad del producto" "gRPC"
            3: sistema.orders -> sistema.dbOrders "Guarda pedido y detalles"

            autoLayout lr
        }
        
         dynamic sistema "D_Consulta_Protegida" {
            title "Flujo - Consulta protegida de pedidos con JWT"

            1: cliente -> sistema.gateway "Consulta un pedido con JWT" "HTTP/GraphQL"
            2: sistema.gateway -> sistema.orders "Obtiene el pedido solicitado" "HTTP/JSON"
            3: sistema.gateway -> sistema.clients "Consulta el cliente asociado al pedido" "HTTP/JSON"

            autoLayout lr
        }


        styles {
            element "Person" {
                shape person
                background #56718A
                color #FFFFFF
            }

            element "Software System" {
                shape roundedbox
                background #173B5D
                color #FFFFFF
            }

            element "Container" {
                shape roundedbox
                background #DCEAF7
                color #173B5D
            }

            element "Database" {
                shape cylinder
                background #E5EAF0
                color #243F56
            }
        }
    }
}
