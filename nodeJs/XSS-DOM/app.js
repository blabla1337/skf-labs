const express = require("express");
const app = express();

app.use(express.static(__dirname + "/static"));

app.get("", (req, res) => {
  res.render("index.ejs");
});

app.use(function (req, res) {
  res.status(404).render("404.ejs");
});

const port = process.env.PORT || 5000;

app.listen(port, () => console.log(`Listening on port ${port}...!!!`));
