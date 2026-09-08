const express = require('express');
const mongoose = require('mongoose');

const { ApolloServer, gql } = require('apollo-server-express');
const Usuario = require('./models/usuario');

const app = express();

mongoose.connect('mongodb://127.0.0.1:27017/bdunab2')
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
    }

    input UsuarioInput {
        nombre: String!
        pass: String!
    }

    type Alert {
        message: String
    }

    type Query {
        getUsuarios: [Usuario]
        getUsuariosById(id: ID!): Usuario
    }

    type Mutation {
        addUsuario(input: UsuarioInput): Usuario
        updateUsuario(id: ID!, input: UsuarioInput): Usuario
        delUsuario(id: ID!): Alert
    }
`;

const resolvers = {
    Query: {
        async getUsuarios() {
            const usuarios = await Usuario.find();
            return usuarios;
        },

        async getUsuariosById(obj, { id }) {
            const usuario = await Usuario.findById(id);

            if (usuario == null) {
                return null;
            }

            return usuario;
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
                { new: true }
            );

            return usuario;
        },

        async delUsuario(obj, { id }) {
            await Usuario.findByIdAndDelete(id);

            return {
                message: 'Usuario eliminado'
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