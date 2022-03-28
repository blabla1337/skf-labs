const express = require("express");
const jwt = require("jsonwebtoken");
const app = express();

app.use(express.static(__dirname + "/static"));
app.use(express.urlencoded({ extended: true }));
app.use(express.json());

class User {
  constructor(id, username, password, role) {
    this.id = id;
    this.username = username;
    this.password = password;
  }
}

let users = [new User(1, "admin", "admin"), new User(2, "user2", "abcxyz")];

const secret = "secret";

const authenticate = (username, password) => {
  let user = users.find((user) => user.username === username);
  if (user && user.password === password) {
    return user;
  }
};

const identity = (payload) => {
  let user = users.find((user) => user.id === payload.id);
  if (user) {
    return user;
  }
};

app.get("", (req, res) => {
  res.render("index.ejs");
});

app.get("/protected", (req, res) => {
  const token = req.headers.authorization.split(" ")[1];
  let claims = jwt.verify(token, secret);
  let user = identity(claims);
  return res.send(`userId: ${user.id}`);
});

app.post("/auth", (req, res) => {
  const user = authenticate(req.body.username, req.body.password);
  if (user) {
    const token = jwt.sign({ id: user.id }, secret, {
      expiresIn: "1h",
    });
    res.json({
      access_token: token,
    });
  }
});

app.use(function (req, res) {
  res.status(404).render("404.ejs");
});

const port = process.env.PORT || 5000;

app.listen(port, "0.0.0.0", () => console.log(`Listening on port ${port}...!!!`));

/* const token = req.headers.authorization.split(" ")[1];
  console.log(token); */
