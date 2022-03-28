const cookieSession = require("cookie-session");
const express = require("express");
const sqlite3 = require("sqlite3").verbose();
const cookieParser = require("cookie-parser");
const app = express();
const db = new sqlite3.Database("./Database.db3");

app.set("view engine", "ejs");
app.use(express.static(__dirname + "/static"));
app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use(cookieParser());
app.use(
  cookieSession({
    name: "session",
    keys: ["e5ac-4ebf-03e5-9e29-a3f562e10b22"],
    maxAge: 86400000,
  })
);

app.get("", (req, res) => {
  res.render("index.ejs");
});

app.all("/login", (req, res) => {
  const sql = "SELECT * FROM users WHERE username = ? AND password = ?";
  const api = "SELECT * FROM preferences WHERE UserId = ?";
  if (req.method === "POST") {
    db.get(sql, [req.body.username, req.body.password], (err, row) => {
      if (row) {
        req.session.userId = row.UserId;
        req.session.secret = "e5ac-4ebf-03e5-9e29-a3f562e10b22";
        req.session.loggedIn = true;
        db.get(api, [req.session.userId], (err, row) => {
          res.render("home.ejs", { api: row.API_key });
        });
      } else {
        res.render("index.ejs");
      }
    });
  } else {
    db.get(api, [req.session.userId], (err, row) => {
      res.render("home.ejs", { api: row.API_key });
    });
  }
});

app.use(function (req, res) {
  res.status(404).render("404.ejs");
});

const port = process.env.PORT || 5000;

app.listen(port, "0.0.0.0", () => console.log(`Listening on port ${port}...!!!`));
