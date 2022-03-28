const express = require("express");
const app = express();
const libxml = require("libxmljs");

app.use(express.static(__dirname + "/static"));
app.use(express.urlencoded({ extended: true }));

app.get("", (req, res) => {
  res.render("index.ejs", { nodes: null });
});

app.post("/home", (req, res) => {
  let xxe = req.body.xxe;
  try {
    doc = libxml.parseXml(xxe, { noent: true });
    res.render("index.ejs", { nodes: doc.toString() });
  } catch (err) {
    console.log(err);
    res.render("index.ejs", { nodes: null });
  }
});

app.use(function (req, res) {
  res.status(404).render("404.ejs");
});

const port = process.env.PORT || 5000;

app.listen(port, "0.0.0.0", () => console.log(`Listening on port ${port}...!!!`));
