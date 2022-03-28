const express = require("express");
const app = express();

app.use(express.static(__dirname));
app.use(express.urlencoded({ extended: true }));

app.get("/:path", (req, res) => {
  res.sendFile("/script_provider/" + req.params.path);
});

const port = process.env.PORT || 8081;

app.listen(port, "0.0.0.0", () => console.log(`Listening on port ${port}...!!!`));
