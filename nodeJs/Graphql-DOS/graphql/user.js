const graphql = require("graphql");
const sqlite3 = require("sqlite3").verbose();
const database = new sqlite3.Database("./db.sqlite");

const UserType = new graphql.GraphQLObjectType({
  name: "User",
  fields: () => ({
    id: { type: graphql.GraphQLID },
    username: { type: graphql.GraphQLString },
    posts: {
      type: PostType,
      resolve: (parent, args) => {
        return new Promise((resolve, reject) => {
          database.get(
            `SELECT * FROM posts WHERE id = ?`,
            [parent.id],
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

module.exports = UserType;

// Bypassing circular dependency errors

const PostType = require("./post");
