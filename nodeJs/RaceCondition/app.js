const express = require("express");
const app = express();
const { exec } = require("child_process");
const { execSync } = require("child_process");
const fs = require("fs");

app.use(express.static(__dirname + "/static"));
app.use(express.urlencoded({ extended: true }));

app.get("/", (req, res) => {
  let hello = "";
  let action = req.query.action ? req.query.action : "run";
  if (action === "validate") {
    let person = req.query.person ? req.query.person : "Default User";
    let valid = boot_validate(person);
    if (valid == "") {
      boot_clean();
    }
  } else if (action == "reset") {
    boot_clean();
    boot_reset();
    boot_run();
  } else {
    boot_run();
    try {
      hello = fs.readFileSync("hello.txt", "utf8").toString();
    } catch (error) {
      hello = "Important hello file is missing, please reset.";
      boot_clean();
      boot_reset();
      boot_run();
    }
  }
  res.render("index.ejs", { action: action, hello: hello });
});

app.use(function (req, res) {
  res.status(404).render("404.ejs");
});

const boot_validate = (person) => {
  fs.writeFileSync("hello.sh", 'echo "' + person + '" > hello.txt');
  exec("echo 'hello.sh updated -- " + Date.now() + "' > log.txt");
  exec("echo 'hello.sh cleaned -- " + Date.now() + "' >> log.txt");
  exec("bash hello.sh");
  const valid = () => {
    return execSync(
      "sed -n '/^echo \"[A-Za-z0-9 ]*\" > hello.txt$/p' hello.sh"
    ).toString();
  };
  return valid();
};

const boot_clean = () => {
  exec(`rm hello.txt`);
};

const boot_run = () => {
  exec(`bash hello.sh`);
};

const boot_reset = () => {
  fs.writeFileSync("hello.sh", "echo 'Default User' > hello.txt");
};

const port = process.env.PORT || 5000;

app.listen(port, "0.0.0.0", () => console.log(`Listening on port ${port}...!!!`));
