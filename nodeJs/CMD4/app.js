const express = require("express");
const app = express();
const { exec } = require("child_process");
const fs = require("fs");

app.use(express.static(__dirname + "/static"));
app.use(express.urlencoded({ extended: true }));

app.get("", (req, res) => {
  res.render("index.ejs", { read: null });
});

app.post("/", (req, res) => {
  let ip = req.body.text;
  ip = ip.replace("`", "");
  ip = ip.replace(";", "");
  ip = ip.replace("&", "");
  exec(`ping -c1 ${ip} > ./ping_output`);

  setTimeout(() => {
    fs.readFile("ping_output", "utf8", (err, data) => {
      console.log(data);
      res.render("index.ejs", { read: data });
    });
  }, 9000);
});

app.use(function (req, res) {
  res.status(404).render("404.ejs");
});

const port = process.env.PORT || 5000;

app.listen(port, "0.0.0.0", () => console.log(`Listening on port ${port}...!!!`));
