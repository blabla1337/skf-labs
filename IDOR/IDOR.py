from flask import Flask, request, url_for, render_template, send_file
import requests
from fpdf import FPDF
import random

app = Flask(__name__, static_url_path = '/static', static_folder = 'static')
app.config['DEBUG'] = True

pdf_ids= random.sample(range(0, 1500), 600)
create_pdf_pool()

def generate_pdf(id, message):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(40, 10, message)
    pdf.output(id + '.pdf', 'F')

def create_pdf_pool():
    # generate a bunch of dummy pdf files    

    for id in pdf_ids[:]:
        generate_pdf(id, 'Try again!')

    # generate the secret pdf
    generate_pdf(pdf_ids[ramdom.randint(600)], 'You have found the secret pdf. Congratulations!')
 
@app.route("/")
def start():
    create_pdf_pool()
    return render_template("index.html")

@app.route("/download", methods = ['POST'])
def download():
    pdf_id = request.form['pdf_id']
    if (pdf_id in dummy_ids):
    	return send_from_directory(directory="./", filename=pdf_id + '.pdf', mimetype='application/pdf')
    else:
        return render_template("index.html", result = "Pdf not found. Try with another id between 500 and 1500.")

@app.route("/create", methods = ['POST'])
def create():
    message = request.form['message']

    while True:
        new_id = ramdon.randint(0, 1500)
    if new_id not in pdf_ids:
        pdf_ids.add(new_id)
        generate_pdf(new_id, message)
    else:
        return render_template("index.html", result = "Pdf created successfully! ID:" + new_id)
 
if __name__ == "__main__":
  app.run(host = '0.0.0.0')
