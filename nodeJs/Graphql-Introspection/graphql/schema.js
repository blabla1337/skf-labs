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

const queryType = new graphql.GraphQLObjectType({
  name: "Query",
  fields: {
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
  },
});

const schema = new graphql.GraphQLSchema({
  query: queryType,
});

module.exports = {
  schema,
};
