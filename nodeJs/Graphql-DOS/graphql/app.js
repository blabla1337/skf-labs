const express = require("express");
const ExpressGraphQL = require("express-graphql").graphqlHTTP;
const schema = require("./graphql/schema.js");
const app = express();

app.use("/graphql", ExpressGraphQL({ schema: schema.schema, graphiql: true }));
app.use(express.static(__dirname + "/static"));
app.use(express.urlencoded({ extended: true }));
app.use(express());
app.use(express.json());

app.get("", (req, res) => {
  res.render("index.ejs");
});

app.listen(5000, "0.0.0.0", () => {
  console.log("Server running at http://localhost:5000.");
});
