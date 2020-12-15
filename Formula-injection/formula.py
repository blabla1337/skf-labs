from models.sqlimodel import *
from flask import Flask, request, url_for, render_template, redirect
import flask_excel as excel


app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config['DEBUG'] = True

excel.init_excel(app)


@app.route("/", methods=['GET'])
def home():
    p = Pages()
    menu = p.getAllPages()
    return render_template("index.html", menu=menu)


@app.route("/home/<pageId>", methods=['GET'])
def inject(pageId):
    if pageId == 0:
        pageId = 1
    p  = Pages()
    values = p.getPage(pageId)
    id      = values[0][0]
    title   = values[0][1]
    content = values[0][2]

    menu = p.getAllPages()

    return render_template("index.html",title = title, content = content, id = id, menu = menu)

@app.route("/pages/add", methods=['POST'])
def add():
    p = Pages()
    msg = p.addPage(request.form.get('title'),request.form.get('content'))
    menu = p.getAllPages()
    return render_template("index.html", menu=menu, msg = msg)

@app.route("/pages/export", methods=['GET'])
def export():
    p = Pages()
    menu = p.getAllPages()
    pagesArray = []
    pagesArray.append(["Page ID","Title","Content"])
    for page in menu:
        pagesArray.append([page[0],page[1],page[2]])
        
    return excel.make_response_from_array(pagesArray,"xls",file_name="export_pages")    

@app.route("/pages/clear", methods=['GET'])
def clear():
    p = Pages()
    msg = p.clearPages()
    menu = p.getAllPages()
    return render_template("index.html", menu=menu, msg = msg)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
	