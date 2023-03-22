# Parameter binding

## Running the app on Docker

```
$ sudo docker pull blabla1337/owasp-skf-lab:js-parameterbinding
```

```
$ sudo docker run -ti -p 127.0.0.1:5000:5000 blabla1337/owasp-skf-lab:js-parameterbinding
```

{% hint style="success" %}
Now that the app is running let's go hacking!
{% endhint %}

## Reconnaissance

Mass assignment is a computer vulnerability where an active record pattern in a web application is abused to modify data items that the user should not normally be allowed to access such as password, granted permissions, or administrator status.

Many web application frameworks offer an active record and object-relational mapping features, where external data in serialization formats is automatically converted on input into internal objects and, in turn, into database record fields. If the framework's interface for that conversion is too permissive and the application designer doesn't mark specific fields as immutable, it is possible to overwrite fields that were never intended to be modified from outside (e.g. admin permissions flag).

This attack is mostly really hard to recognize and identify since we can't tell
by simply looking at an application that it might be utilizing an ORM framework.

Mostly for each popular programming language there is an ORM available

| Programming language | ORM framework    |
| -------------------- | ---------------- |
| PHP laravel          | Eloquent         |
| Python               | SQLAlchemy       |
| Ruby                 | ActiveRecord     |
| C#                   | Entity framework |
| Java                 | Hibernate        |

Now, the summerization above just scratches the surface for all the different ORM
that are out there in the wild.

This type of attack is also possible if the application is using an ODM (Object Document Mapping), the difference being ODM is used with NoSQL databases. A very popular ODM for nodeJs is mongoose, which is used for a MongoDB database.

In order to determine the stack that is running on the webserver we first need to
do active reconnaissance on the webserver and application.

The fingerprinting is out of scope for this excersise but more information about the
topic is found here:

{% hint style="info" %}
https://www.owasp.org/index.php/Fingerprint_Web_Server_(OTG-INFO-002)
https://www.owasp.org/index.php/Fingerprint_Web_Application_Framework_(OTG-INFO-008)
{% endhint %}

By inspecting the source code of the target application we find
that it utlizes an ODM framework to write queries to the database.

```javascript
const mongoose = require("mongoose");

const UserSchema = new mongoose.Schema({
  username: {
    type: String,
    required: true,
    minlength: 2,
    maxlength: 20,
  },
  password: {
    type: String,
    required: true,
  },
  is_admin: {
    type: Boolean,
    default: false,
  },
});

const User = mongoose.model("User", UserSchema);

module.exports = User;
```

Please take note of the following code in the UserRoutes.js . This line of code will prove critical for exploiting the parameter binding attack.

```javascript
app.post("/create", upload.none(), async (req, res) => {
  const user = new UserModel(req.body); // HERE IS THE PROBLEM
  try {
    await user.save();
    res.render("index.ejs", { msg: "User created successfully" });
  } catch (error) {
    res.status(500).send(error);
  }
});
```

## Exploitation

Now, let's examine the target application and determine the objective.

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/nodejs/ParameterBinding/1.png)

Let's log in with one of the credentials the application is suggesting.

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/nodejs/ParameterBinding/2.png)

If we logout and go back to the home page we see an option to register a new user.

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/nodejs/ParameterBinding/3.png)

Let's register a new user and check the request on Burp.

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/nodejs/ParameterBinding/4.png)

As we saw in this line of code:

```javascript
const user = new UserModel(req.body);
```

The application is creating a new User using the OBM UserModel with req.body instead of using Object destructuring to extract only the username and password.
Maybe if we add another parameter in the request this parameter will also pass to our new User.

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/nodejs/ParameterBinding/5.png)

Now if we login.

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/nodejs/ParameterBinding/6.png)

Bingo! We have now created a new user with Admin privileges.

## Additional sources

Please refer to the OWASP cheat sheet for a full complete description about parameter binding attacks.

{% embed url="https://cheatsheetseries.owasp.org/cheatsheets/Mass_Assignment_Cheat_Sheet.html" %}

{% embed url="https://en.wikipedia.org/wiki/Mass_assignment_vulnerability" %}
