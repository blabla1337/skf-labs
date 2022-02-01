const graphql = require("graphql");
const sqlite3 = require("sqlite3").verbose();
const database = new sqlite3.Database("./db.sqlite");
const UserType = require("./user");
const PostType = require("./post");

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
