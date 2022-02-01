const express = require("express");
const ldap = require("ldapjs");
const { exec } = require("child_process");
const multer = require("multer");
const { timeout } = require("nodemon/lib/config");
const app = express();
const upload = multer({});

app.set("view engine", "ejs");
app.use(express.static(__dirname + "/static"));
app.use(express.urlencoded({ extended: true }));

// start the LDAP server - need root privileges

exec("chmod +x ./glauth32", (shell = true));
exec("sh run_ldap_server.sh", (shell = true));

// connect to the LDAP server
const client = ldap.createClient({ url: "ldap://127.0.0.1:389" });
client.bind("cn=ldapadmin,ou=accounts,dc=com", "mysecret", (err) => {});

const authenticate = (req, res) => {
  const username = req.body.username;
  const password = req.body.secret_answer;
  const options = {
    scope: "sub",
    filter: "(&(cn=" + username + ")(sn=" + password + "))",
  };
  let result_content = null;
  try {
    client.search("ou=accounts,dc=com", options, (err, result) => {
      if (err) {
        res.render("index", { result: "Invalid username or password" });
      }
      result.on("searchEntry", (entry) => {
        result_content = entry.object;
      });
      result.on("end", (result) => {
        result_content
          ? res.render("index", { result: "You are now admin user!" })
          : res.render("index", { result: "Invalid username or password" });
      });
    });
  } catch (error) {
    res.render("index", { result: "Invalid username or password" });
  }
};

app.get("", (req, res) => {
  res.render("index.ejs", { result: null });
});

app.post("/login", upload.none(), (req, res) => {
  const secret = req.body.secret_answer;
  secret.length < 2
    ? res.render("index", { result: "Invalid username or password" })
    : authenticate(req, res);
});

app.use(function (req, res) {
  res.status(404).render("404.ejs");
});

const port = process.env.PORT || 5000;

app.listen(port, () => console.log(`Listening on port ${port}...!!!`));
