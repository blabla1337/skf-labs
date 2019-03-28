from flask import Flask, render_template, redirect, url_for, request, session

app = Flask(__name__)
app.config['SECRET_KEY'] = "fp)73lql-0t_d#9&szqs8&e_ic*mm6v7%!siamgfmq#gkr(a=+"
@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'devteam' or request.form['password'] != 'manchesterunited':
            error = 'Invalid Credentials. Please try again.'
            session['logged_in'] = False
        else:
            session['logged_in'] = True 
            return render_template("pwned.html")
    return render_template('login.html', error=error)

@app.route('/pwned/')
def secret():
     if  session['logged_in'] == True:
         return render_template("pwned.html")
     elif session['logged_in'] == False:
         return render_template("login.html")
         
if __name__== "__main__":
    app.run(host='0.0.0.0')


    
