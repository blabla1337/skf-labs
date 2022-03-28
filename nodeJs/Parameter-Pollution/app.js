const cookieSession = require("cookie-session");
const express = require("express");
const sqlite3 = require("sqlite3").verbose();
const cookieParser = require("cookie-parser");
const session = require("express-session");
const app = express();
const db = new sqlite3.Database("./Database.db3");
const { body, validationResult } = require("express-validator");

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

app.get("/home", (req, res) => {
  const sql = "SELECT * FROM users WHERE userId = ?";
  if (session.isLoggedIn) {
    db.get(sql, [session.userId], (err, row) => {
      row ? res.render("home.ejs", { email: row.Email }) : res.redirect("/");
    });
  } else {
    res.redirect("/");
  }
});

app.post("/login", (req, res) => {
  const sql = "SELECT * FROM users WHERE username = ? AND password = ?";
  const api = "SELECT * FROM preferences WHERE UserId = ?";
  db.get(sql, [req.body.username, req.body.password], (err, row) => {
    if (row) {
      session.userId = row.UserId;
      session.isLoggedIn = true;
      res.redirect("/home");
    } else {
      res.redirect("/");
    }
  });
});

app.post("/update", body("email").isEmail(), (req, res) => {
  const errors = validationResult(req);
  const sql = "UPDATE users SET email = ? WHERE userId = ?";
  if (!errors.isEmpty()) {
    res.redirect("/home");
  } else {
    db.run(sql, [req.body.email, session.userId], (err) => {
      res.redirect("/home");
    });
  }
});

app.use(function (req, res) {
  res.status(404).render("404.ejs");
});

const port = process.env.PORT || 5000;

app.listen(port, "0.0.0.0", () => console.log(`Listening on port ${port}...!!!`));
