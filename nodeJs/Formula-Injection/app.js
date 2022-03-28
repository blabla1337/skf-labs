const express = require("express");
const sqlite3 = require("sqlite3").verbose();
const app = express();
const XLSX = require("xlsx");
const db = new sqlite3.Database("./Database.db3");

app.use(express.static(__dirname + "/static"));
app.use(express.urlencoded({ extended: true }));

app.get("/", async (req, res) => {
  const sql = "SELECT * FROM pages";
  db.all(sql, (err, rows) => {
    res.render("index.ejs", {
      menu: rows,
    });
  });
});

app.get("/home/:pageId", async (req, res) => {
  req.params.pageId == "0" ? (req.params.pageId = "1") : req.params.pageId;
  const pageId = req.params.pageId - 1;
  console.log("XXXX : " + pageId);
  const sql = "SELECT * FROM pages WHERE pageId = ?";
  db.all("SELECT * FROM pages", (err, rows) => {
    let page = rows[pageId];
    res.render("index.ejs", {
      menu: rows,
      id: page.pageId,
      title: page.title,
      content: page.content,
    });
  });
});

app.post("/pages/add", (req, res) => {
  const title = req.body.title;
  const content = req.body.content;
  db.run(
    "INSERT INTO pages VALUES(?,?,?)",
    [null, title, content],
    (err) => {}
  );
  db.all("SELECT * FROM pages", (err, rows) => {
    res.render("index.ejs", {
      menu: rows,
      msg: "Page added successfully",
    });
  });
});

app.get("/pages/export", (req, res) => {
  const sql = "SELECT * FROM pages";
  db.all(sql, (err, rows) => {
    let pagesArray = [];
    pagesArray.push(["pageId", "title", "content"]);
    rows.forEach((page) => {
      pagesArray.push([page.pageId, page.title, page.content]);
    });
    const wb = XLSX.utils.book_new();
    const ws = XLSX.utils.aoa_to_sheet(pagesArray);
    XLSX.utils.book_append_sheet(wb, ws, "pages");
    XLSX.writeFile(wb, "pages.xlsx");
    res.download("pages.xlsx");
  });
});

app.get("/pages/clear", (req, res) => {
  db.run("DELETE FROM pages WHERE pageId > 3");
  db.all("SELECT * FROM pages", (err, rows) => {
    res.render("index.ejs", {
      menu: rows,
      msg: "Pages cleared successfully",
    });
  });
});

app.use(function (req, res) {
  res.status(404).render("404.ejs");
});

const port = process.env.PORT || 5000;

app.listen(port, "0.0.0.0", () => console.log(`Listening on port ${port}...!!!`));
