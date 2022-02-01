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
    keys: ["secret"],
    maxAge: 86400000,
  })
);

let session;

app.get("", (req, res) => {
  res.render("index.ejs");
});

app.post("/login", (req, res) => {
  const username = req.body.username;
  const password = req.body.password;
  const sql = "SELECT * FROM users WHERE username = ? AND password = ?";
  const sql_prefs = "SELECT * FROM prefs WHERE userId = ?";
  db.get(sql, [username, password], (err, row) => {
    if (row) {
      session = req.session;
      session.userId = row.UserId;
      session.loggedIn = true;
      db.get(sql_prefs, [session.userId], (err, row) => {
        res.render("loggedin.ejs", { color: row.Color, food: row.Food });
      });
    } else {
      res.render("index.ejs");
    }
  });
});

app.get("/updatecolor", (req, res) => {
  const sql = "SELECT * FROM prefs WHERE userId = ?";
  if (!session.loggedIn) {
    res.render("index.ejs");
  } else {
    db.get(sql, [session.userId], (err, row) => {
      res.render("loggedin.ejs", { color: row.Color, food: row.Food });
    });
  }
});

app.post("/updatecolor", (req, res) => {
  if (!session.loggedIn) {
    res.render("index.ejs");
  }

  const color = req.body.color;
  const sql = "UPDATE prefs SET Color = ? WHERE UserId = ?";
  const sql_food = "SELECT Food FROM prefs WHERE UserId = ?";
  db.run(sql, [color, session.userId]);
  db.get(sql_food, [session.userId], (err, row) => {
    res.render("loggedin.ejs", { color: color, food: row.Food });
  });
});

app.post("/updatefood", (req, res) => {
  if (!session.loggedIn) {
    res.render("index.ejs");
  }

  const food = req.body.food;
  const sql = "UPDATE prefs SET Food = ? WHERE UserId = ?";
  const sql_color = "SELECT Color FROM prefs WHERE UserId = ?";
  db.run(sql, [food, session.userId]);
  db.get(sql_color, [session.userId], (err, row) => {
    res.render("loggedin.ejs", { color: row.Color, food: food });
  });
});

app.use(function (req, res) {
  res.status(404).render("404.ejs");
});

const port = process.env.PORT || 5000;

app.listen(port, () => console.log(`Listening on port ${port}...!!!`));
