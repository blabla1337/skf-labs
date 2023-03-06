const express = require("express");
const app = express();
const fileUpload = require("express-fileupload");
const { exec } = require("child_process");
const fs = require("fs");

app.use(express.static(__dirname + "/static"));
app.use(express.urlencoded({ extended: true }));
app.use(fileUpload({ uriDecodeFileNames: true }));


system_call = (cmd) => {
    let cmdoutput = cmd + " > ./output";
    exec(cmdoutput, (error, stdout, stderr) => {
      if (error) {
          //console.log(`error: ${error.message}`);
          return error.message;
      }
      if (stderr) {
          //console.log(`stderr: ${stderr}`);
          return stderr;
      }
      //console.log(`stdout: ${stdout}`);
      return stdout
    });
};

const ALLOWED_EXTENSIONS = ["txt", "pdf", "png", "jpg", "jpeg", "html", "ejs"];

const allowed_file = (filename) => {
  const extension = filename.split(".").pop();
  return ALLOWED_EXTENSIONS.includes(extension);
};

app.get("/", async (req, res) => {
  setTimeout(() => {
    fs.readFile("output", "utf8", (err, data) => {
      console.log(data);
      res.render("index.ejs", { uploaded: null, cmdresponse: data });
    });
  }, 2000);
});

app.post("/", async (req, res) => {
  const file = req.files.file;
  const filePath = "upload/" + file.name;
  console.log(file);
  console.log(filePath);
  if (file && allowed_file(file.name)) {
    file.mv(filePath, async (err) => {
      if (err) return res.status(500).send(err);
      res.render("index.ejs", { uploaded: "File uploaded successfully", cmdresponse: null });
    });
  } else {
    res.render("index.ejs", { uploaded: "File not allowed", cmdresponse: null });
  }
});

app.use(function (req, res) {
  res.status(404).render("404.ejs");
});

const port = process.env.PORT || 5000;

app.listen(port, "0.0.0.0", () => console.log(`Listening on port ${port}...!!!`));
