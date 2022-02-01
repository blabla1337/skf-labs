const cookieSession = require("cookie-session");
const express = require("express");
const cookieParser = require("cookie-parser");
const app = express();

app.use(express.static(__dirname + "/static"));
app.use(cookieParser());
app.use(
  cookieSession({
    name: "session",
    keys: ["e5ac-4ebf-03e5-9e29-a3f562e10b22"],
    httpOnly: false,
    maxAge: 86400000,
  })
);

app.get("", (req, res) => {
  req.session.userId = 2;
  req.session.secret = "e5ac-4ebf-03e5-9e29-a3f562e10b22";
  req.session.loggedIn = true;
  console.log(req.session);
  res.render("evil.ejs");
});

const port = process.env.PORT || 1337;

app.listen(port, () => console.log(`Listening on port ${port}...!!!`));
