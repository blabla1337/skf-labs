const express = require("express");
const app = express();

app.use(express.static(__dirname + "/static"));
app.use(express.urlencoded({ extended: true }));

app.get("", (req, res) => {
  res.render("evil.ejs");
});

app.use(function (req, res) {
  res.status(404).render("404.ejs");
});

const port = process.env.PORT || 1337;

app.listen(port, () => console.log(`Listening on port ${port}...!!!`));
