const express = require("express");
const app = express();
const http = require("http");
const { exec } = require("child_process");

app.use(express.static(__dirname + "/static"));
app.use(express.urlencoded({ extended: true }));

app.get("", (req, res) => {
  res.render("index.ejs", { result: null });
});

app.post("/cmd", (req, res) => {
  let filename = req.body.filename;
  let filepath = "";
  if (!filename.includes("http")) {
    let host = req.protocol + "://" + req.get("host");
    filepath = host + "/" + filename;
  } else {
    filepath = filename;
  }
  try {
    http.get(filepath, (result) => {
      result.setEncoding("utf8");
      result.on("data", (body) => {
        let ev = eval(body);
        ev.stdout.on("data", (data) => {
          res.render("index.ejs", { result: data });
        });
      });
    });
  } catch (error) {
    console.log(error);
    res.render("index.ejs", {
      result:
        "Unexpected error during the execution of the predefined command.",
    });
  }
});

app.use(function (req, res) {
  res.status(404).render("404.ejs");
});

const port = process.env.PORT || 5000;

app.listen(port, "0.0.0.0", () => console.log(`Listening on port ${port}...!!!`));
