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

const valid_login = (username, password) => {
  const sql = `SELECT * FROM emptbl WHERE UserName = ? AND Password = ?`;
  return new Promise((resolve, reject) => {
    db.get(sql, [username, password], (err, row) => {
      if (err) {
        return reject(err);
      }
      if (row) {
        return resolve(true);
      } else {
        return resolve(false);
      }
    });
  });
};

const valid_login_forgot = (username) => {
  const sql = `SELECT * FROM emptbl WHERE UserName = ?`;
  return new Promise((resolve, reject) => {
    db.get(sql, [username], (err, row) => {
      if (err) {
        return reject(err);
      }
      if (row) {
        return resolve(true);
      } else {
        return resolve(false);
      }
    });
  });
};

app.get("", (req, res) => {
  res.render("index.ejs", { error: null });
});

app.all("/login", async (req, res) => {
  let error = "";
  const validLogin = await valid_login(req.body.username, req.body.password);
  if (req.method === "POST") {
    if (validLogin) {
      req.session.log = true;
      res.render("dashboard.ejs", { username: req.body.username });
    } else {
      error = "Invalid username or password";
      res.render("index.ejs", { error: error });
    }
  } else {
    error = null;
    res.render("index.ejs", { error: error });
  }
});

app.all("/forgot", async (req, res) => {
  let error = "";
  let validLoginForgot = await valid_login_forgot(req.body.username);
  if (req.method === "POST") {
    if (validLoginForgot) {
      req.session.log = true;
      error =
        "If your username is registered with us,  you will receive an email with the new password";
      res.render("forgot.ejs", { error: error });
    } else {
      error =
        "If your username is registered with us,  you will receive an email with the new password";
      res.render("forgot.ejs", { error: error });
    }
  } else {
    error = null;
    res.render("forgot.ejs", { error: error });
  }
});

app.get("/dashboard", (req, res) => {
  if (!req.session.log) {
    res.redirect("/");
  } else {
    if (valid_login_forgot(req.session.username)) {
      res.render("dashboard.ejs", { username: req.session.username });
    } else {
      res.redirect("/forgot");
    }
  }
});

app.get("/logout", (req, res) => {
  req.session = null;
  res.render("index.ejs", { error: null });
});

app.use(function (req, res) {
  res.status(404).render("404.ejs");
});

const port = process.env.PORT || 5000;

app.listen(port, "0.0.0.0", () => console.log(`Listening on port ${port}...!!!`));
