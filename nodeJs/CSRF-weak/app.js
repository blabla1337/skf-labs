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
  db.get(sql, [username, password], (err, row) => {
    if (row) {
      const date = new Date();
      const time = date.getHours() + ":" + date.getMinutes();
      let csrf_token = username + time;
      session = req.session;
      session.userId = row.UserId;
      session.loggedIn = true;
      session.csrf_token = Buffer.from(csrf_token).toString("base64");
      db.get("SELECT * FROM preferences", (err, row) => {
        row
          ? res.render("home.ejs", {
              color: row.Color,
              csrf_token: session.csrf_token,
            })
          : res.render("home.ejs", { color: null, csrf_token: null });
      });
    } else {
      res.render("");
    }
  });
});

app.post("/update", (req, res) => {
  if (!session.loggedIn) {
    res.render("");
  } else {
    const sql = "UPDATE preferences SET Color = ? WHERE UserId = ?";
    db.run(sql, [req.body.color, req.session.userId], (err) => {
      if (err) {
        console.log(err);
      } else {
        db.get("SELECT * FROM preferences", (err, row) => {
          if (req.session.csrf_token === req.body.csrf_token) {
            res.render("home.ejs", {
              color: row.Color,
              csrf_token: req.body.csrf_token,
            });
          } else {
            res.render("home.ejs", { color: null, csrf_token: null });
          }
        });
      }
    });
  }
});

app.use(function (req, res) {
  res.status(404).render("404.ejs");
});

const port = process.env.PORT || 5000;

app.listen(port, () => console.log(`Listening on port ${port}...!!!`));
