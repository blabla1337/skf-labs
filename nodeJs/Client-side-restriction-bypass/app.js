const express = require("express");
const app = express();

app.use(express.static(__dirname + "/static"));
app.use(express.urlencoded({ extended: true }));

app.get("", (req, res) => {
  res.render("index.ejs", { read: null });
});

app.post("/", (req, res) => {
  let output = "";
  let sleepTime = req.body.numero;
  if (sleepTime < 7 && sleepTime >= 3) {
    output = output = "You should sleep more";
  } else if (sleepTime >= 7 && sleepTime < 10) {
    output = "You sleep a proper while";
  } else if (sleepTime > 9 && sleepTime <= 13) {
    output = "You should sleep less";
  } else {
    output = "That's not possible... HACKER!!!";
  }
  res.render("index.ejs", { read: output });
});

app.use(function (req, res) {
  res.status(404).render("404.ejs");
});

const port = process.env.PORT || 5000;

app.listen(port, "0.0.0.0", () => console.log(`Listening on port ${port}...!!!`));
