const graphql = require("graphql");
const sqlite3 = require("sqlite3").verbose();
const database = new sqlite3.Database("./db.sqlite");

const UserType = new graphql.GraphQLObjectType({
  name: "User",
  fields: {
    id: { type: graphql.GraphQLID },
    username: { type: graphql.GraphQLString },
    isAdmin: { type: graphql.GraphQLBoolean },
  },
});

const PostType = new graphql.GraphQLObjectType({
  name: "Post",
  fields: {
    id: { type: graphql.GraphQLID },
    title: { type: graphql.GraphQLString },
    body: { type: graphql.GraphQLString },
    author_id: { type: graphql.GraphQLID },
    users: {
      type: UserType,
      resolve: (parent, args) => {
        return new Promise((resolve, reject) => {
          database.get(
            `SELECT * FROM users WHERE id = ${parent.author_id}`,
            (err, row) => {
              if (err) {
                reject(err);
              } else {
                resolve(row);
              }
            }
          );
        });
      },
    },
  },
});

const UserInfoType = new graphql.GraphQLObjectType({
  name: "UserInfo",
  fields: {
    id: { type: graphql.GraphQLID },
    name: { type: graphql.GraphQLString },
    surname: { type: graphql.GraphQLString },
    date_of_birth: { type: graphql.GraphQLString },
    api_key: { type: graphql.GraphQLString },
    user: { type: graphql.GraphQLInt },
  },
});

var queryType = new graphql.GraphQLObjectType({
  name: "Query",
  fields: {
    User: {
      type: UserType,
      args: {
        username: { type: graphql.GraphQLString },
      },
      resolve: (root, args) => {
        return new Promise((resolve, reject) => {
          database.get(
            `SELECT * FROM users WHERE username = "${args.username}"`,
            (err, row) => {
              if (err) reject(err);
              else resolve(row);
            }
          );
        });
      },
    },

    Users: {
      type: new graphql.GraphQLList(UserType),
      resolve: (root, args, context, info) => {
        return new Promise((resolve, reject) => {
          database.all("SELECT * FROM Users;", function (err, rows) {
            if (err) {
              reject([]);
            }
            resolve(rows);
          });
        });
      },
    },

    Posts: {
      type: new graphql.GraphQLList(PostType),
      resolve: (root, args, context, info) => {
        return new Promise((resolve, reject) => {
          database.all("SELECT * FROM Posts;", function (err, rows) {
            if (err) {
              reject([]);
            }
            resolve(rows);
          });
        });
      },
    },
    UserInfo: {
      type: UserInfoType,
      args: { id: { type: graphql.GraphQLID } },
      resolve: (root, args) => {
        return new Promise((resolve, reject) => {
          database.get(
            `SELECT * FROM User_Info WHERE id = ${args.id}`,
            (err, row) => {
              if (err) {
                reject(err);
              } else {
                resolve(row);
              }
            }
          );
        });
      },
    },
  },
});

const schema = new graphql.GraphQLSchema({
  query: queryType,
});

module.exports = {
  schema,
};
