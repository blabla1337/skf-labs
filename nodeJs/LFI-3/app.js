const express = require("express");
const app = express();
const fs = require("fs");

app.use(express.static(__dirname + "/static"));
app.use(express.urlencoded({ extended: true }));

app.get("", (req, res) => {
  res.render("index.ejs", { file: null });
});

app.post("/home", (req, res) => {
  let filename = req.body.filename;
  filename = decodeURIComponent(filename);
  if (!filename.includes("../")) {
    filename = decodeURIComponent(filename);
    fs.readFile(filename, "utf8", (err, data) => {
      if (err) {
        res.render("index.ejs", { file: "Try harder!" });
        return;
      }
      res.render("index.ejs", { file: data });
    });
  } else {
    res.render("index.ejs", { file: "Try harder!" });
  }
});

app.use(function (req, res) {
  res.status(404).render("404.ejs");
});

const port = process.env.PORT || 5000;

app.listen(port, "0.0.0.0", () => console.log(`Listening on port ${port}...!!!`));
