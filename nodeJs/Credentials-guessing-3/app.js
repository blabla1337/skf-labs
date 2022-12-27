const express = require("express");
const sqlite3 = require("sqlite3").verbose();
const cookieParser = require("cookie-parser");
const sessions = require("express-session");
const app = express();
const db = new sqlite3.Database("./Database.db3");

app.set("view engine", "ejs");
app.use(express.static(__dirname + "/static"));
app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use(cookieParser());
app.use(
  sessions({
    secret: "secret",
    resave: false,
    saveUninitialized: true,
    cookie: { maxAge: 86400000 },
  })
);

let session;

app.get("", (req, res) => {
  res.render("index.ejs", { error: null });
});

app.post("/login", (req, res) => {
  const username = req.body.username;
  const password = req.body.password;
  const sql = "SELECT * FROM users WHERE username = ?";
  db.get(sql, [username], (err, row) => {
    if (row) {
      if (row.Password == password) {
        session = req.session;
        session.userId = row.UserId;
        session.loggedIn = true;
        res.render("home.ejs");
      } else {
        res.render("", {
          error:
            "Password is incorrect                                                ",
        });
      }
    } else {
      res.render("", { error: "Username does not exist" });
    }
  });
});

app.use(function (req, res) {
  res.status(404).render("404.ejs");
});

const port = process.env.PORT || 5000;

app.listen(port, "0.0.0.0", () =>
  console.log(`Listening on port ${port}...!!!`)
);
