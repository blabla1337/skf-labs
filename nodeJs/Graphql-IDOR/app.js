const express = require("express");
const ExpressGraphQL = require("express-graphql").graphqlHTTP;
const schema = require("./graphql/schema.js");
const sqlite3 = require("sqlite3").verbose();
const db = new sqlite3.Database("./db.sqlite");
const cookies = require("cookie-parser");
const app = express();

app.use("/graphql", ExpressGraphQL({ schema: schema.schema, graphiql: true }));
app.use(express.static(__dirname + "/static"));
app.use(express.urlencoded({ extended: true }));
app.use(express());
app.use(express.json());
app.use(cookies());

app.get("", (req, res) => {
  const api_key = req.cookies["X-Api-Key"];
  const api_sql = "SELECT * FROM user_info WHERE api_key = ?";
  db.get(api_sql, [api_key], (err, row) => {
    row
      ? res.render("index.ejs", { username: row.name + " " + row.surname })
      : res.redirect("/login");
  });
});

app.get("/login", (req, res) => {
  res.render("login.ejs", { error: null });
});

app.post("/login", (req, res) => {
  const username = req.body.username;
  const password = req.body.password;
  const sql = "SELECT * FROM users WHERE username = ? AND password = ?";
  const api_sql = "SELECT api_key FROM user_info WHERE user = ?";
  db.get(sql, [username, password], (err, row) => {
    if (row) {
      console.log(row);
      db.get(api_sql, [row.id], (err, result) => {
        res.cookie("X-Api-Key", result.api_key);
        res.cookie("id", row.id);
        res.render("index.ejs", { username: row.name + " " + row.surname });
      });
    } else {
      res.render("login.ejs", { error: "Invalid username or password" });
    }
  });
});

app.get("/settings", (req, res) => {
  const api_key = req.cookies["X-Api-Key"];
  const api_sql = "SELECT * FROM user_info WHERE api_key = ?";
  db.get(api_sql, [api_key], (err, row) => {
    row
      ? res.render("settings.ejs", { username: row.name })
      : res.redirect("/login");
  });
});

app.listen(5000, "0.0.0.0", () => {
  console.log("Server running at http://localhost:5000.");
});
