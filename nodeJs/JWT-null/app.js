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
    this.role = role;
  }
}

let users = [
  new User(1, "user", "user", "guest"),
  new User(2, "user2", "user2", "mortal"),
  new User(3, "immortal", "immortal", "admin"),
];

const secret = "VerylongUnbreakablesecretbecausebruteforceisnotthecase";

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
  let claims;
  const token = req.headers.authorization.split(" ")[1];
  const jwt_header = token.split(".")[0];
  const decode_jwt_header = Buffer.from(jwt_header, "base64").toString();
  const headers = JSON.parse(decode_jwt_header);
  if (headers.alg == "NONE") {
    claims = jwt.decode(token, { complete: false });
  } else {
    claims = jwt.verify(token, secret);
  }
  let user = identity(claims);
  let ret = `Welcome ${user.username}: ${user.role}`;
  return res.send(ret);
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
