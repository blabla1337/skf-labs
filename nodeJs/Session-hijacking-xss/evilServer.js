const express = require("express");
const app = express();

app.use(express.static(__dirname + "/static"));
app.use(express.urlencoded({ extended: true }));

app.get("/", (req, res) => {
  console.log(req.query);
  res.render("evil.ejs");
});

const port = process.env.PORT || 1337;

app.listen(port, "0.0.0.0", () => console.log(`Listening on port ${port}...!!!`));
