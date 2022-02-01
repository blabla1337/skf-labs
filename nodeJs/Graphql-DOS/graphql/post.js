const graphql = require("graphql");
const sqlite3 = require("sqlite3").verbose();
const database = new sqlite3.Database("./db.sqlite");

const PostType = new graphql.GraphQLObjectType({
  name: "Post",
  fields: () => ({
    id: { type: graphql.GraphQLID },
    title: { type: graphql.GraphQLString },
    body: { type: graphql.GraphQLString },
    author_id: { type: graphql.GraphQLID },
    users: {
      type: UserType,
      resolve: (parent, args) => {
        return new Promise((resolve, reject) => {
          database.get(
            `SELECT * FROM users WHERE id = ?`,
            [parent.author_id],
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
  }),
});

module.exports = PostType;

// Bypassing circular dependency errors

const UserType = require("./user");
