const cookieSession = require("cookie-session");
const express = require("express");
const sqlite3 = require("sqlite3").verbose();
const cookieParser = require("cookie-parser");
const app = express();
const db = new sqlite3.Database("./Database.db3");
const crypto = require("crypto");

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

app.get("", (req, res) => {
  res.render("index.ejs");
});

app.get("/register", (req, res) => {
  res.render("register.ejs", { msg: null });
});

app.get("/loggedin", (req, res) => {
  let txt = "You have to be logged in to see this page!";
  let msg = " Find the way to login as an admin!";
  if (req.cookies.sessionId) {
    hash = req.cookies.sessionId;
    sql = "SELECT * FROM users WHERE Hash = ?";
    db.get(sql, [hash], (err, row) => {
      if (row) {
        if (row.UserName == "admin") {
          res.render("loggedin.ejs", {
            msg: "Congratulations!",
            username: row.UserName,
          });
        } else {
          res.render("loggedin.ejs", { msg: txt, username: row.UserName });
        }
      } else {
        res.render("loggedin.ejs", { msg: msg, username: null });
      }
    });
  } else {
    res.render("loggedin.ejs", { msg: txt, username: null });
  }
});

app.post("/create", (req, res) => {
  const username = req.body.username.trim().toLowerCase();
  const password = req.body.password.trim();
  const hash = crypto
    .createHash("sha1")
    .update(req.body.username + "SKFowaspLabs")
    .digest("hex");
  const sql = "SELECT * FROM users WHERE username = ?";
  if (username != "" && password != "") {
    db.get(sql, [username], (err, row) => {
      if (row) {
        res.render("register.ejs", { msg: "Username already exists" });
      } else {
        const sql =
          "INSERT INTO users (username, password, hash) VALUES (?, ?, ?)";
        db.run(sql, [username, password, hash], () => {
          res.render("index.ejs", { msg: "Account created" });
        });
      }
    });
  } else {
    res.render("register.ejs", { msg: "Please fill in all fields" });
  }
});

app.all("/login", (req, res) => {
  const sql = "SELECT * FROM users WHERE username = ? AND password = ?";
  if (req.method === "POST") {
    db.get(sql, [req.body.username, req.body.password], (err, row) => {
      if (row) {
        req.session.userId = row.UserId;
        req.session.loggedIn = true;
        res.cookie(
          "sessionId",
          crypto
            .createHash("sha1")
            .update(req.body.username + "SKFowaspLabs")
            .digest("hex")
        );
        res.render("home.ejs", {
          username: req.body.username,
          msg: "Find the way to login as an admin!",
        });
      } else {
        res.render("index.ejs");
      }
    });
  } else {
    res.render("index.ejs");
  }
});

app.get("/about", (req, res) => {
  res.render("about.ejs");
});

app.get("/logout", (req, res) => {
  req.session = null;
  res.clearCookie("sessionId");
  res.render("index.ejs");
});

app.use(function (req, res) {
  res.status(404).render("404.ejs");
});

const port = process.env.PORT || 5000;

app.listen(port, () => console.log(`Listening on port ${port}...!!!`));
