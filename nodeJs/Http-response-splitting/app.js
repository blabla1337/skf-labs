const express = require("express");
const app = express();

app.use(express.static(__dirname + "/static"));
app.use(express.urlencoded({ extended: true }));

app.get("/", (req, res) => {
  res.render("index2.ejs");
});

app.get("/web", (req, res) => {
  let sleepingtime = req.query.numero;
  res.render("index.ejs", { read: sleepingtime });
});

app.use(function (req, res) {
  res.status(404).render("404.ejs");
});

const port = process.env.PORT || 5000;

app.listen(port, () => console.log(`Listening on port ${port}...!!!`));
