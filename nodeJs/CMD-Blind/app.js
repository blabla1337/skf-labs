const express = require("express");
const app = express();
const { exec } = require("child_process");

app.use(express.static(__dirname + "/static"));
app.use(express.urlencoded({ extended: true }));

app.get("", (req, res) => {
  res.render("index.ejs", { read: null });
});

app.post("/", (req, res) => {
  let text_input = req.body.text;
  exec(`echo ${text_input} >> welcome`);
  let text = "WELCOME!";
  res.render("index.ejs", { read: text });
});

app.use(function (req, res) {
  res.status(404).render("404.ejs");
});

const port = process.env.PORT || 5000;

app.listen(port, "0.0.0.0", () => console.log(`Listening on port ${port}...!!!`));
