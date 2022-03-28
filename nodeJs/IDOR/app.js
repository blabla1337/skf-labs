const express = require("express");
const app = express();
const PDFDocument = require("pdfkit");
const fs = require("fs");

app.use(express.static(__dirname + "/static"));
app.use(express.urlencoded({ extended: true }));

let pdf_ids = Array.from({ length: 60 }, () => Math.floor(Math.random() * 100));

const generate_pdf = (id, message) => {
  const doc = new PDFDocument();
  doc.pipe(fs.createWriteStream(id.toString() + ".pdf"));
  doc.fontSize(25).text(message);
  doc.end();
};

const generate_pdf_pool = () => {
  pdf_ids.forEach((id) => {
    generate_pdf(id, "Try Again!");
  });
  generate_pdf(
    Math.floor(Math.random() * 60),
    "You have found the secret pdf, congratulations!"
  );
};

app.get("/", (req, res) => {
  generate_pdf_pool();
  res.render("index.ejs", { result: null });
});

app.post("/download", (req, res) => {
  const id = req.body.pdf_id;
  if (pdf_ids.includes(parseInt(id))) {
    let pdf_name = id.toString() + ".pdf";
    res.download(pdf_name);
  } else {
    res.render("index.ejs", {
      result: "Pdf not found. Try with another id between 1 and 1500.",
    });
  }
});

app.post("/create", (req, res) => {
  const msg = req.body.message;
  while (pdf_ids.length < 1500) {
    let new_id = Math.floor(Math.random() * 1500);
    if (!pdf_ids.includes(new_id)) {
      generate_pdf(new_id, msg);
      pdf_ids.push(new_id);
      return res.render("index.ejs", {
        result: `Pdf created successfully! ID: ${new_id.toString()}`,
      });
    }
  }
  return res.render("index.ejs", { result: null });
});

app.use(function (req, res) {
  res.status(404).render("404.ejs");
});

const port = process.env.PORT || 5000;

app.listen(port, "0.0.0.0", () => console.log(`Listening on port ${port}...!!!`));
