import os
import datetime
from flask import Flask, request, url_for, render_template, redirect


app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config['DEBUG'] = True

@app.route("/")
def start():
	hello = ""
	action = request.values.get('action') if request.values.get('action') else "run"
	if action == "validate":
		person = request.values.get('person') if request.values.get('person') else "Default User"
		valid = boot_validate(person)
		if valid == "":
			boot_clean()
	elif action == "reset":
		boot_clean()
		boot_reset()
	else:
		boot_run()
		try:
			hello = open("hello.txt","r").read()
		except:
			hello = "Important hello file is missing, please reset."
			boot_clean()
			boot_reset()
			boot_run()
	return render_template("index.html", hello=hello, action=action)

def boot_validate(person):
	#person = person.replace('"',"").replace("\\","")
	bootfile = open("hello.sh","w")
	bootfile.write("echo \"" + person + "\" > hello.txt")
	bootfile.close()

	os.system("echo 'hello.sh updated -- " + str(datetime.datetime.now()) + "' > log.txt")
	valid = os.popen("sed -n '/^echo \"[A-Za-z0-9 ]*\" > hello.txt$/p' hello.sh").read()
	os.system("echo 'hello.sh cleaned -- " + str(datetime.datetime.now()) + "' >> log.txt")

	return valid

def boot_clean():
	os.system("rm hello.*")

def boot_run():
	os.system("bash hello.sh")

def boot_reset():
	bootfile = open("hello.sh","w")
	bootfile.write("echo \"Default User\" > hello.txt")
	bootfile.close()

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")@app.errorhandler(404)


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', threaded=True)

