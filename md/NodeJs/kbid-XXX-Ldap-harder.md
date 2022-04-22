# KBID xxx - Ldap Injection - harder

## Running the app nodeJs

First make sure nodejs and npm are installed on your host machine.
After installation, we go to the folder of the lab we want to practice.
"i.e /skf-labs/XSS, /skf-labs/RFI/" and run the following commands:

```
$ npm install
```

```
$ npm start
```

Now that the app is running let's go hacking!

## Reconnaissance

LDAP Injection is an attack used to exploit web based applications that construct LDAP statements based on user input. When an application fails to properly sanitize user input, it’s possible to modify LDAP statements using a local proxy. This could result in the execution of arbitrary commands such as granting permissions to unauthorized queries, and content modification inside the LDAP tree. The same advanced exploitation techniques available in SQL Injection can be similarly applied in LDAP Injection.

Let's open the app.

![](../../.gitbook/assets/nodejs/Ldap/Ldap-1.png)

Trying to loggin with a random username and password.

![](../../.gitbook/assets/nodejs/Ldap/Ldap-2.png)

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

![](../../.gitbook/assets/nodejs/Ldap-harder/Ldap-4.png)

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

![](../../.gitbook/assets/nodejs/Ldap-harder/Ldap-5.png)

We successfully logged in as the Admin.

## Additional sources

{% embed url="https://owasp.org/www-community/attacks/LDAP_Injection" %}

{% embed url="https://cheatsheetseries.owasp.org/cheatsheets/LDAP_Injection_Prevention_Cheat_Sheet.html" %}

{% embed url="https://www.synopsys.com/glossary/what-is-ldap-injection.html" %}

{% embed url="https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/LDAP%20Injection/README.md" %}
