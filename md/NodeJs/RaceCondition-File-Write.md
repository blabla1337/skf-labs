# Race Condition File-Write

## Running the app on Docker

```
$ sudo docker pull blabla1337/owasp-skf-lab:js-racecondition-file-write
```

```
$ sudo docker run -ti -p 127.0.0.1:5000:5000 blabla1337/owasp-skf-lab:js-racecondition-file-write
```

{% hint style="success" %}
Now that the app is running let's go hacking!
{% endhint %}

## Reconnaissance

#### Step1

We can download a file from the server by doing a GET request to the server.

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/python/RaceCondition-file-write/1.png)

Let's try:

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/python/RaceCondition-file-write/2.png)

Once we download the file we can see whatever we add to the URL is being written in a file called shared-file.

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/python/RaceCondition-file-write/3.png)

#### Step 2

As the application suggests, there is a Race condition vulnerability in this app, let's try to find it.

If we look at the code we see that the application gets the query parameter, writes to a file called shared-file.txt, then opens the file and send it back as a response.

```javascript
app.get("/:value", (req, res) => {
  fs.writeFileSync("shared-file.txt", req.params.value);
  fs.open("shared-file.txt", "r", (err, fd) => {
    let file = fs.readFileSync("shared-file.txt", "utf8");
    res.setHeader("Content-Type", "text/html", "charset=utf-8");
    res.setHeader(
      "Content-Disposition",
      "attachment; filename=shared-file.txt"
    );
    res.sendFile(__dirname + "/shared-file.txt");
  });
});
```

#### Step 3

We have a very small window between the writing of the file:

```javascript
fs.writeFileSync("shared-file.txt", req.params.value);
```

and the response:

```javascript
fs.open("shared-file.txt", "r", (err, fd) => {
  let file = fs.readFileSync("shared-file.txt", "utf8");
  res.setHeader("Content-Type", "text/html", "charset=utf-8");
  res.setHeader("Content-Disposition", "attachment; filename=shared-file.txt");
  res.sendFile(__dirname + "/shared-file.txt");
});
```

Maybe if we have multiple users on this application at the same time we might be able to intercept someone else's query.

## Exploitation

In order to do that we must send requests with high frequency.

Doing it manually is practically impossible, so we create a script that does that for us:

```sh

#!/bin/bash

while true; do

	curl -i -s -k  -X $'GET' -H $'Host: localhost:5000' $'http://localhost:5000/111' | grep "111"

done

```

and in the meantime we will send a couple requests from Burp:

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/python/RaceCondition-file-write/4.png)

If we look in the logs we will see:

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/python/RaceCondition-file-write/5.png)

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/python/RaceCondition-file-write/6.png)

## Additional sources

https://wiki.owasp.org/index.php/Testing_for_Race_Conditions_(OWASP-AT-010)
