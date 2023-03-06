const express = require("express");
const app = express();
const request = require('request');
const URL = require("url").URL;
const { exec } = require("child_process");

app.use(express.static(__dirname + "/static"));
app.use(express.urlencoded({ extended: true }));

exec("/bin/bash run_services.sh", (error, stdout, stderr) => {
  if (error) {
      console.log(`error: ${error.message}`);
      return;
  }
  if (stderr) {
      console.log(`stderr: ${stderr}`);
      return;
  }
  console.log(`stdout: ${stdout}`);
});


const stringIsAValidUrl = (s, protocols) => {
  try {
      url = new URL(s);
      return protocols
          ? url.protocol
              ? protocols.map(x => `${x.toLowerCase()}:`).includes(url.protocol)
              : false
          : true;
  } catch (err) {
      return false;
  }
};

app.get("", (req, res) => {
  res.render("index.ejs", { frontmessage: null });
});

app.post("/check_existence", (req, res) => {
  const url = req.body.url;
  if (!stringIsAValidUrl(url, ['http', 'https'])) {
    res.render("index.ejs", { frontmessage: "The URL schema is not valid." });
  }
  request.head(url, { timeout: 2000 }, (error) => {
    if (error) {
      if (error.code === 'ECONNREFUSED') {
        res.render("index.ejs", { frontmessage: "Target resource is not reachable." });
      } else {
        res.render("index.ejs", { frontmessage: "Target resource is reachable!" });
      }
    } else {
      res.render("index.ejs", { frontmessage: "Webpage found!" });
    }
  });
});


app.use(function (req, res) {
  res.status(404).render("404.ejs");
});

const port = process.env.PORT || 5000;

app.listen(port, "0.0.0.0", () => console.log(`Listening on port ${port}...!!!`));
//childProcess.execSync("bash run_services.sh")
