const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');

const {ApolloServer, gql} = require('apollo-server-express');
const Usuario = require('./models/usuario');

mongoose.connect('mongodb://localhost:27017/bdunab2');
const typDefs = gql`
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
        async getUsuarios(obj) {
            const usuarios = await Usuario.find();
            return usuarios;
        },
        async getUsuariosById(obj, {id}) {
            const usuario = await Usuario.findById(id);
            if (usuarioBus == null) {
                return null;
            } else {
                return usuario;
            }
        }
    },
    Mutation: {
        async addUsuario(obj, {input}) {
            const usuario = new Usuario(input);
            await usuario.save();
            return usuario;
        },
        async updateUsuario(obj, {id, input}) {
            const usuario = await Usuario.findByIdAndUpdate(id, input);
            return usuario;
        },
        async delUsuario(obj, {id}) {
            await Usuario.findByIdAndDelete(id);
            return {
                message: 'Usuario eliminado'
            };
        }
    }
};    

let apolloServer = null;
const corsOptions = {
    origin: 'http://localhost:8090',
    credentials: false
};

async function startServer() {
    apolloServer = new ApolloServer({
        typeDefs: typDefs,
        resolvers: resolvers,
        cors: corsOptions
    });
    await apolloServer.start();
    apolloServer.applyMiddleware({app, path: false});
}
startServer();

const app = express();
app.use(cors());
app.listen(8090, function() {
    console.log('GraphQL iniciado');
});