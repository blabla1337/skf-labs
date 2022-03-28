const express = require("express");
const app = express();
const fs = require("fs");

app.use(express.static(__dirname + "/static"));
app.use(express.urlencoded({ extended: true }));

app.get("/", (req, res) => {
  res.render("index.ejs", { mode: null, os_result: null, print_result: null });
});

app.get("/:value", (req, res) => {
  fs.writeFileSync("shared-file.txt", req.params.value);
  fs.open("shared-file.txt", "r", (err, fd) => {
    let file = fs.readFileSync("shared-file.txt", "utf8");
    res.setHeader("Content-Type", "text/html", "charset=utf-8");
    res.setHeader(
      "Content-Disposition",
      "attachment; filename=shared-file.txt"
    );
    res.sendFile(__dirname + "/shared-file.txt");
  });
});

app.use(function (req, res) {
  res.status(404).render("404.ejs");
});

const port = process.env.PORT || 5000;

app.listen(port, "0.0.0.0", () => console.log(`Listening on port ${port}...!!!`));
