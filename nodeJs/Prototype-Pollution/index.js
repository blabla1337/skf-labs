const express = require("express");
const multer = require("multer");
const _ = require("lodash");
const Joi = require("joi");
const validate = require("express-validation");
const upload = multer();
const app = express();

app.set("view engine", "ejs");
app.use(express.static(__dirname + "/static"));
app.use(express.urlencoded({ extended: true }));
app.use(express.json());

const postSchema = {
  body: Joi.object({
    email: Joi.string().email().required(),
    msg: Joi.string().required(),
  }),
};

const users = [
  (admin = {
    username: "admin",
    password: "admin",
    admin: true,
  }),
  (user = {
    username: "user",
    password: "user",
    admin: false,
  }),
];

let session = {};

app.get("", (req, res) => {
  session = {};
  res.render("index", { msg: null });
});

app.get("/register", (req, res) => {
  res.render("register.ejs");
});

app.post("/create", upload.none(), (req, res) => {
  const { username, password } = req.body;
  let newUser = { username, password };
  users.push(newUser);
  res.render("index.ejs", { msg: "User created" });
});

app.post("/message", validate(postSchema), (req, res) => {
  const obj = _.merge({}, req.body, { ipAddress: req.ip });
  res.redirect("/login");
});

app.post("/login", upload.none(), (req, res) => {
  const { username, password } = req.body;
  const user = users.find((user) => user.username === username);
  if (user && user.password === password) {
    session.username = user.username;
    session.isLoggedIn = true;
    res.render("loggedin.ejs", {
      username: user.username,
      admin: user.admin,
    });
  } else {
    res.render("index.ejs", { msg: "Login failed" });
  }
});

app.get("/login", (req, res) => {
  const user = users.find((user) => user.username === session.username);
  session.isLoggedIn
    ? res.render("loggedin.ejs", {
        username: user.username,
        admin: user.admin,
      })
    : res.render("index.ejs", { msg: "Please login" });
});

const port = process.env.PORT || 5000;

app.listen(port, "0.0.0.0", () => console.log(`Listening on port ${port}...!!!`));
