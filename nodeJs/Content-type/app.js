const express = require("express");
const app = express();
const multer = require("multer");
const upload = multer({});

app.use(express.static(__dirname + "/static"));
app.use(express.urlencoded({ extended: true }));

app.get("", (req, res) => {
  res.render("index.ejs", { xss: null });
});

app.post("/unprotected", upload.none(), (req, res) => {
  let val = req.body.no_header;
  let xss = JSON.stringify({ key: val, key2: "another value" });
  res.render("index.ejs", { xss: xss });
});

app.post("/protected", upload.none(), (req, res) => {
  let val = req.body.with_header;
  console.log(val);
  let xss = JSON.stringify({ key: val, key2: "another value" });
  console.log(xss);
  res.setHeader("Content-type", "application/json");
  res.render("index.ejs", { xss: xss });
});

app.use(function (req, res) {
  res.status(404).render("404.ejs");
});

const port = process.env.PORT || 5000;

app.listen(port, () => console.log(`Listening on port ${port}...!!!`));
