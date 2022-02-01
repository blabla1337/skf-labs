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

const mutationType = new graphql.GraphQLObjectType({
  name: "Mutation",
  fields: {
    createPost: {
      type: PostType,
      args: {
        title: {
          type: new graphql.GraphQLNonNull(graphql.GraphQLString),
        },
        body: {
          type: new graphql.GraphQLNonNull(graphql.GraphQLString),
        },
        author_id: { type: new graphql.GraphQLNonNull(graphql.GraphQLID) },
      },
      resolve: (root, { title, body, author_id }) => {
        return new Promise((resolve, reject) => {
          database.run(
            "INSERT INTO Posts (title, body, author_id) VALUES (?,?,?);",
            [title, body, author_id],
            (err) => {
              if (err) {
                reject(null);
              }
              database.get("SELECT last_insert_rowid() as id", (err, row) => {
                resolve({
                  id: row["id"],
                  title: title,
                  body: body,
                  author_id: author_id,
                });
              });
            }
          );
        });
      },
    },
  },
});

const schema = new graphql.GraphQLSchema({
  query: queryType,
  mutation: mutationType,
});

module.exports = {
  schema,
};
