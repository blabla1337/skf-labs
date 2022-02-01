const express = require("express");
const mongoose = require("mongoose");
const userRouter = require("./routes/UserRoutes");
const app = express();

app.use(express.static(__dirname + "/static"));
app.use(express.urlencoded({ extended: true }));
app.use(express.json());

// This application database is running on MongoAtlas, in case you want to connect to a local database or your own database, change the following:
mongoose.connect(
  "mongodb+srv://user:supersecret@cluster0.gcznz.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
);

app.get("", (req, res) => {
  res.render("index.ejs", { msg: null });
});

app.get("/register", (req, res) => {
  res.render("register.ejs");
});

app.use(userRouter);

app.use(function (req, res) {
  res.status(404).render("404.ejs");
});

const port = process.env.PORT || 5000;

app.listen(port, () => console.log(`Listening on port ${port}...!!!`));
