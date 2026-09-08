const express = require('express');
const mongoose = require('mongoose');

const { ApolloServer, gql } = require('apollo-server-express');

const Usuario = require('./models/usuario');
const Producto = require('./models/producto');

const app = express();


mongoose.connect('mongodb://127.0.0.1:27017/dulcehogar')
    .then(() => {
        console.log('MongoDB conectado');
    })
    .catch((error) => {
        console.log('Error al conectar MongoDB:');
        console.log(error);
    });


const typeDefs = gql`

    type Usuario {
        id: ID!
        nombre: String!
        pass: String!
        rol: String!
    }

    input UsuarioInput {
        nombre: String!
        pass: String!
        rol: String!
    }

    type Producto {
        id: ID!
        nombre: String!
        categoria: String!
        precio: Float!
        stock: Int!
    }

    input ProductoInput {
        nombre: String!
        categoria: String!
        precio: Float!
        stock: Int!
    }

    type Alert {
        message: String
    }


    type Query {

        getUsuarios: [Usuario]
        getUsuarioById(id: ID!): Usuario

        getProductos: [Producto]
        getProductoById(id: ID!): Producto
    }


    type Mutation {


        addUsuario(input: UsuarioInput): Usuario

        updateUsuario(
            id: ID!,
            input: UsuarioInput
        ): Usuario

        delUsuario(id: ID!): Alert



        addProducto(input: ProductoInput): Producto

        updateProducto(
            id: ID!,
            input: ProductoInput
        ): Producto

        delProducto(id: ID!): Alert
    }
`;


const resolvers = {

    Query: {

        async getUsuarios() {

            const usuarios = await Usuario.find();

            return usuarios;
        },

        async getUsuarioById(obj, { id }) {

            const usuario = await Usuario.findById(id);

            if (usuario == null) {
                return null;
            }

            return usuario;
        },


        async getProductos() {

            const productos = await Producto.find();

            return productos;
        },


        async getProductoById(obj, { id }) {

            const producto = await Producto.findById(id);

            if (producto == null) {
                return null;
            }

            return producto;
        }
    },


    Mutation: {

        async addUsuario(obj, { input }) {

            const usuario = new Usuario(input);

            await usuario.save();

            return usuario;
        },

        async updateUsuario(obj, { id, input }) {

            const usuario = await Usuario.findByIdAndUpdate(
                id,
                input,
                {
                    new: true
                }
            );

            return usuario;
        },


        async delUsuario(obj, { id }) {

            await Usuario.findByIdAndDelete(id);

            return {
                message: 'Usuario eliminado'
            };
        },


        async addProducto(obj, { input }) {

            const producto = new Producto(input);

            await producto.save();

            return producto;
        },


        async updateProducto(obj, { id, input }) {

            const producto = await Producto.findByIdAndUpdate(
                id,
                input,
                {
                    new: true
                }
            );

            return producto;
        },

        async delProducto(obj, { id }) {

            await Producto.findByIdAndDelete(id);

            return {
                message: 'Producto eliminado'
            };
        }
    }
};


async function startServer() {

    const apolloServer = new ApolloServer({
        typeDefs,
        resolvers
    });

    await apolloServer.start();

    apolloServer.applyMiddleware({
        app,
        path: '/graphql',
        cors: {
            origin: 'https://studio.apollographql.com',
            credentials: false
        }
    });

    app.listen(8090, () => {

        console.log('GraphQL iniciado');
        console.log('Servidor: http://localhost:8090/graphql');

    });
}

startServer();