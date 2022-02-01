const express = require("express");
const app = express();
const { exec } = require("child_process");
const fs = require("fs");

app.use(express.static(__dirname + "/static"));
app.use(express.urlencoded({ extended: true }));

app.get("/", (req, res) => {
  res.render("index.ejs", { mode: null, os_result: null, print_result: null });
});

app.post("/compress", (req, res) => {
  const mode = "compress";
  const log_type = req.body.log_type;
  const os_result = exec(
    "zip log.zip " +
      log_type +
      "_log.txt && echo ' --> \
		Log file successfully compressed to log.zip'"
  );
  os_result.stdout.on("data", (data) => {
    res.render("index.ejs", {
      mode: mode,
      os_result: data,
    });
  });
});

app.post("/viewer", (req, res) => {
  const red_lines = (line) => {
    line = line.split(":");
    return "<font color='red'>" + line[0] + "</font>: " + line[1] + "<br/>";
  };
  const blue_lines = (line) => {
    line = line.split(":");
    return (
      "<font color='blue'><b>" + line[0] + "</b></font>: " + line[1] + "<br/>"
    );
  };
  const normal_lines = (line) => {
    return line + "<br/>";
  };
  const mode = "viewer";
  const log_files = ["access", "error"];
  let print_result = "";
  const lines_type = req.body.lines;
  for (let log_file of log_files) {
    print_result +=
      "<div style='border: thin solid black;padding: 10px;display: inline-block;'><b>" +
      log_file +
      "_log.txt</b></div><br/><br/>";
    for (let line of fs
      .readFileSync(log_file + "_log.txt")
      .toString()
      .split("\n")) {
      print_result += eval(lines_type + "_lines")(line);
    }
  }
  res.render("index.ejs", { mode: mode, print_result: print_result });
});

app.use(function (req, res) {
  res.status(404).render("404.ejs");
});

const port = process.env.PORT || 5000;

app.listen(port, () => console.log(`Listening on port ${port}...!!!`));
