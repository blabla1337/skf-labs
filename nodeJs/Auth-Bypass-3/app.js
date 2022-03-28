const express = require("express");
const app = express();

app.set("view engine", "ejs");
app.use(express.static(__dirname + "/static"));
app.use(express.urlencoded({ extended: true }));

app.get("", (req, res) => {
  res.render("index.ejs");
});

app.post("/signup", (req, res) => {
  let username = req.body.username.trim().toLowerCase();
  res.render("user_created_right.ejs", { username: username });
});

app.get("/users/:user_id", (req, res) => {
  let user_id = req.params.user_id;
  if (user_id == "user01") {
    res.render("user_account.ejs", {
      username: "bob",
      password: "abc123",
      data: "Your secret message: [STILL NOT SET]",
    });
  } else if (user_id == "user02") {
    res.render("user_account.ejs", {
      username: "admin",
      password: "rootadmin",
      data: "I am the admin of this website",
    });
  } else {
    res.render("user_account_empty.ejs", {
      username: "You need to set your usser account",
      password: "You need to set your password",
      data: "You need to set your data",
    });
  }
});

app.use(function (req, res) {
  res.status(404).render("404.ejs");
});

const port = process.env.PORT || 5000;

app.listen(port, "0.0.0.0", () => console.log(`Listening on port ${port}...!!!`));
