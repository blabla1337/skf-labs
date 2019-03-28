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
    password = request.form['password']

    search_filter = "(&(cn="+username+")(sn="+password+"))"
    try:    
        result_content = ""
        result_content = ldap_connection.search_s("dc=com", ldap.SCOPE_SUBTREE, search_filter)    
        if(len(result_content) == True):
            return render_template("index.html", result = "You are now admin user!")    
        else:
            return render_template("index.html", result = "Wrong identity provided.")
    except Exception as e:
        return render_template("index.html", result = "Wrong identity provided.")
    
if __name__ == "__main__":
  app.run(host = '0.0.0.0')
