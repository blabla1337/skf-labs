# WebSocket Message Manipulation

## Running the app on Docker

```
$ sudo docker pull blabla1337/owasp-skf-lab:websocket-message-manipulation
```

```
$ sudo docker run -ti -p 127.0.0.1:5000:5000 blabla1337/owasp-skf-lab:websocket-message-manipulation
```

{% hint style="success" %}
Now that the app is running let's go hacking!
{% endhint %}

## Reconnaissance

Traditionally, the HTTP protocol only allows one request/response per TCP connection. Asynchronous JavaScript and XML (AJAX) allows clients to send and receive data asynchronously (in the background without a page refresh) to the server, however, AJAX requires the client to initiate the requests and wait for the server responses (half-duplex).

WebSockets allow the client or server to create a ‘full-duplex’ (two-way) communication channel, allowing the client and server to truly communicate asynchronously. WebSockets conduct their initial upgrade handshake over HTTP and from then on all communication is carried out over TCP channels by use of frames.

The goal of this lab is to find some client side vulnerability abusing websockets.

The home paage looks pretty simple:

![](../../.gitbook/assets/python/Websocket-Message-Manipulation/websocket-1.png)

So lets try it by entering some text in input:

![](../../.gitbook/assets/python/Websocket-Message-Manipulation/websocket-2.png)

The application is an echo server. It reflects our input directly on page. The first thing we comes to mind is to check for XSS. Let's try:

![](../../.gitbook/assets/python/Websocket-Message-Manipulation/websocket-3.png)

At the first look, nothing happens and the application shows us two empty rows:

![](../../.gitbook/assets/python/Websocket-Message-Manipulation/websocket-5.png)

Since our input is not empty, it means something happened. Maybe parsed somehow or it's trunicated. To ensure this, let's take a look at the page source code by pressing F12 and use "inspect elemnt" feature of our browser (mine is mozilla firefox):

![](../../.gitbook/assets/python/Websocket-Message-Manipulation/websocket-6.png)

Bingo! our input is right here. So we refresh the page to re-render the entire page and check if inputs are persistent or not:

![](../../.gitbook/assets/python/Websocket-Message-Manipulation/websocket-4.png)

## Exploitation

In this scenario, we capture the request using proxy and manipulate websocket messages as we want. OWASP-ZAP makes it easy to us:

![](../../.gitbook/assets/python/Websocket-Message-Manipulation/websocket-7.png)

As you can see, websocket handshake performed on page load. Let's write some message:

![](../../.gitbook/assets/python/Websocket-Message-Manipulation/websocket-8.png)

Click on "Open/Resend with Message Editor..." option and write your payload:

![](../../.gitbook/assets/python/Websocket-Message-Manipulation/websocket-9.png)

Server respoend us with correctly. Refresh the page to check result:

![](../../.gitbook/assets/python/Websocket-Message-Manipulation/websocket-10.png)

Bingo! we successfully executed code on page. Also we could set breakpoint before sending request ^\_^

NOTE: After refreshing page, you see two alerts per input. The reason is server returns us everything in history and since it's echo server, it duplicates our input. Therefore, popup shown us because of ourselve input in first time, and at the second time it is echo server response that reflacted our message.

## Additional sources

{% embed url="https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/11-Client-side_Testing/10-Testing_WebSockets" %}
{% embed url="https://portswigger.net/web-security/websockets" %}
