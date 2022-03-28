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
    signed: false,
    maxAge: 86400000,
  })
);

let session;

app.get("", (req, res) => {
  res.render("index.ejs");
});

app.post("/login_insecure", (req, res) => {
  const username = req.body.username;
  const password = req.body.password;
  const sql = "SELECT * FROM users WHERE username = ? AND password = ?";
  db.get(sql, [username, password], (err, row) => {
    if (row) {
      session = req.session;
      session.userId = row.UserId;
      session.loggedIn = true;
      db.get("SELECT * FROM preferences", (err, row) => {
        session.color = row.Color;
        res.render("home.ejs", { color: row.Color });
      });
    } else {
      res.render("");
    }
  });
});

app.post("/login_strict", (req, res) => {
  req.sessionOptions.sameSite = "strict";
  const username = req.body.username;
  const password = req.body.password;
  const sql = "SELECT * FROM users WHERE username = ? AND password = ?";
  db.get(sql, [username, password], (err, row) => {
    if (row) {
      session = req.session;
      session.userId = row.UserId;
      session.loggedIn = true;
      db.get("SELECT * FROM preferences", (err, row) => {
        session.color = row.Color;
        res.render("home.ejs", { color: row.Color });
      });
    } else {
      res.render("");
    }
  });
});

app.post("/login_lax", (req, res) => {
  req.sessionOptions.sameSite = "lax";
  const username = req.body.username;
  const password = req.body.password;
  const sql = "SELECT * FROM users WHERE username = ? AND password = ?";
  db.get(sql, [username, password], (err, row) => {
    if (row) {
      session = req.session;
      session.userId = row.UserId;
      session.loggedIn = true;
      db.get("SELECT * FROM preferences", (err, row) => {
        session.color = row.Color;
        res.render("home.ejs", { color: row.Color });
      });
    } else {
      res.render("");
    }
  });
});

app.post("/update", (req, res) => {
  const sql = "UPDATE preferences SET Color = ? WHERE UserId = ?";
  if (!session) {
    res.redirect("/");
  } else {
    db.run(sql, [req.body.color, req.session.userId], (err) => {
      db.get("SELECT * FROM preferences", (err, row) => {
        session.color = row.Color;
        res.render("home.ejs", { color: row.Color });
      });
    });
  }
});

app.get("/update", (req, res) => {
  console.log(req.query);
  if (!session.loggedIn) {
    res.redirect("/");
  } else {
    if (req.query.color) {
      const sql = "UPDATE preferences SET Color = ? WHERE UserId = ?";
      db.run(sql, [req.query.color, req.session.userId], (err) => {
        db.get("SELECT * FROM preferences", (err, row) => {
          session.color = row.Color;
          res.render("home.ejs", { color: row.Color });
        });
      });
    } else {
      res.render("home.ejs", { color: session.color });
    }
  }
});

app.use(function (req, res) {
  res.status(404).render("404.ejs");
});

const port = process.env.PORT || 5000;

app.listen(port, "0.0.0.0", () => console.log(`Listening on port ${port}...!!!`));
