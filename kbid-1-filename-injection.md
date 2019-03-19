# KBID 1 - Path traversal \(LFI\)

## Running the app

```
$ sudo docker pull blabla1337/owasp-skf-lab:filename-injection
```

```text
$ sudo docker run -ti -p 127.0.0.1:5000:5000 blabla1337/owasp-skf-lab:filename-injection
```

{% hint style="success" %}
 Now that the app is running let's go hacking!
{% endhint %}

![Docker Image and write-up thanks to defev!](.gitbook/assets/logo.defdev.1608z.whtonblk.256.png)

## Reconnaissance

#### Step1

The application shows a dropdown menu from which we can choose an intro or chapters to be displayed on the client-side. 

![](.gitbook/assets/screen-shot-2019-01-10-at-12.45.png)

First thing we need to do know is to do more investigation on the requests that are being made. We do this by setting up our intercepting proxy so we can gain more understanding of the application under test.

After we set up our favourite intercepting proxy we are going to look at the traffic between the server and the front-end. the first thing to notice is that it tries to retrieve a text file

![](.gitbook/assets/lfi2.png)

The image above shows the text file that is being fetched from the servers file system highlighted in red. And the response is highlighted in blue.

```python
@app.route("/home", methods=['POST'])
def home():
    filename = request.form['filename']
    if filename == "":
        filename = "default.txt"
    f = open(filename,'r')
    read = f.read()
    return render_template("index.html",read = read)
```

In the code example the "filename" parameter that is used to read content from files of the file system is under the users control. Instead of just reading the intended text files from the file system, a potential attacker could abuse this function to also read other sensitive information from the web server. 

## Exploitation

#### Step1

A potential attacker can now tamper the "filename" parameter to get more sensitive information from the file system. As a proof of concept in a penetration test we will often show a successful attack by getting the "/etc/passwd" file. 

![](.gitbook/assets/lfi3.png)

But other files with sensitive information can of course be just as interesting. How about getting a file with connection strings to the database? It is also not uncommon for administrators to re-use passwords. So retrieving this information could prove to be valuable information to gain access to other systems.

![](.gitbook/assets/screen-shot-2019-01-10-at-12.45.08-sql.png)

## Additional sources

Please refer to the OWASP testing guide for a full complete description about path traversal with all the edge cases over different platforms!

{% embed url="https://www.owasp.org/index.php/Testing\_Directory\_traversal/file\_include\_\(OTG-AUTHZ-001\)" %}

