const express = require("express");
const app = express();
const { exec } = require("child_process");

app.use(express.static(__dirname + "/static"));
app.use(express.urlencoded({ extended: true }));

app.get("", (req, res) => {
  res.render("index.ejs");
});

app.post("/home", (req, res) => {
  const sizeImg = req.body.size;
  exec(`convert static/img/bones.png -resize ${sizeImg}% static/img/bones.png`);
  res.render("index.ejs");
});

app.use(function (req, res) {
  res.status(404).render("404.ejs");
});

const port = process.env.PORT || 5000;

app.listen(port, "0.0.0.0", () =>
  console.log(`Listening on port ${port}...!!!`)
);
