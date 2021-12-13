from flask import Flask, request, render_template
from subprocess import Popen
import ldap
import time

app = Flask(__name__, static_url_path = '/static', static_folder = 'static')
app.config['DEBUG'] = True

# start the LDAP server
Popen("chmod +x ./glauth32", shell=True)
Popen("sh run_ldap_server.sh", shell=True)
time.sleep(5)
# connect to the LDAP server
ldap_connection =ldap.initialize("ldap://127.0.0.1:389")
ldap_connection.simple_bind_s("cn=ldapadmin,ou=accounts,dc=com", "mysecret")

@app.route("/")
def start():
    return render_template("index.html")

@app.route("/login", methods = ['POST'])
def ssrf():
    username = request.form['username']
    secret = request.form['secret_answer']

    if(len(secret) < 2):
        return render_template("index.html", result = "The secret answer is at least 2 character long.")

    search_filter = "(&(cn="+username+")(sn="+secret+"))"
    try:
        result_content = ""
        result_content = ldap_connection.search_s("dc=com", ldap.SCOPE_SUBTREE, search_filter)
        print(result_content)
        
        if(len(result_content) > 0):
            return render_template("index.html", result = "You are now admin user!")
        else:
            return render_template("index.html", result = "Wrong identity provided.")
    except Exception as e:
        return render_template("index.html", result = "Wrong identity provided.")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


if __name__ == "__main__":
  app.run(host = '0.0.0.0')

