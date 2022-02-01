const express = require("express");
var sqlite3 = require("sqlite3").verbose();
const app = express();
var db = new sqlite3.Database("./Database.db3");
app.use(express.static(__dirname + "/static"));

app.get("", (req, res) => {
  res.render("index.ejs", {
    username: null,
    email: null,
  });
});

app.get("/home/:username", (req, res) => {
  let username = req.params.username;
  db.get(
    "SELECT UserName, email FROM users WHERE UserName LIKE '%" +
      username +
      "%' ORDER BY UserId",
    function (err, rows) {
      if (err) {
        res.status(500).end(" " + err);
      } else if (rows == undefined) {
        res.status(404).render("404.ejs");
      } else {
        res.render("index.ejs", {
          username: rows.UserName,
          email: rows.email,
        });
      }
    }
  );
});

app.use((err, req, res, next) => {
  if (!err) return next();
  return res.redirect("/");
});

app.use(function (req, res) {
  res.status(404).render("404.ejs");
});

const port = process.env.PORT || 5000;

app.listen(port, () => console.log(`Listening on port ${port}...!!!`));
