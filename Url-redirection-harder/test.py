def blacklist(url):

	blacklist = [".","/"]

	for b in blacklist:
		if url.find(b):
			return False

	return True

url = "google.com"

a = url.find(".")

print(a)

