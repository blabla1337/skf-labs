const express = require("express");
const UserModel = require("../models/users");
const app = express();
const multer = require("multer");
const upload = multer();

app.post("/login", upload.none(), async (req, res) => {
  const { username, password } = req.body;
  try {
    const user = await UserModel.findOne({ username, password });
    if (user) {
      res.render("loggedin.ejs", {
        username: user.username,
        admin: user.is_admin,
      });
    } else {
      res.status(404).render("404.ejs");
    }
  } catch (error) {
    res.status(500).send(error);
  }
});

app.post("/create", upload.none(), async (req, res) => {
  const user = new UserModel(req.body);
  try {
    await user.save();
    res.render("index.ejs", { msg: "User created successfully" });
  } catch (error) {
    res.status(500).send(error);
  }
});

// GET ALL USERS

/* app.get("/users", async (req, res) => {
  const users = await UserModel.find({});

  try {
    res.send(users);
  } catch (error) {
    res.status(500).send(error);
  }
}); */

module.exports = app;
