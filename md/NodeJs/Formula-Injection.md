# Formula Injection

## Running the app on Docker

```
$ sudo docker pull blabla1337/owasp-skf-lab:js-formula-injection
```

```
$ sudo docker run -ti -p 127.0.0.1:5000:5000 blabla1337/owasp-skf-lab:js-for
```

{% hint style="success" %}
Now that the app is running let's go hacking!
{% endhint %}

## Reconnaissance

### Step1

The first step is to identify input forms and parameters that can be exported as CSV, XLS, XLSX or ODS. In this example we find that it's possible to add new pages and, after clicking on the button "Export pages", generate a XLS report of all pages.

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/python/Formula-Injection/1.png)

```text
http://localhost:5000/
```

### Step2

Now let's see if we can inject a simple spreadsheet formula.

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/python/Formula-Injection/2.png)

```text
=1+1
```

The page "Injection2" was created and the formula was fully accepted.

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/python/Formula-Injection/3.png)

Of course the formula has no effect on browser. This test is important for us to know the application is not validating the operator "=", so it can be used to inject formulas in our spreadsheet.

### Step3

Now, let's export the pages and see in our spreedsheet application (Excel, Calc) how does the formula injection look like.

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/python/Formula-Injection/4.png)

Once the report is loaded into the spreadsheet application, we can notice the formula is not immediatelly executed and it's shown as text. This behavior can vary depending on the version and which application is being used.

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/python/Formula-Injection/5.png)

However, any interaction with the cell containing the injected formula will cause the application to execute it.

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/python/Formula-Injection/6.png)

By doing it so we are sure the application has a Formula Injection vulnerability.

This is due to the fact that the user supplied input is not properly verified, accepting any character, and, thereafter, exports the inputs to a XLS file.

## Exploitation

We are going to use this vulnerability to have a simple Command Execution on the victm's machine.

### Step1

We need to choose the correct formula to inject, based on the spreadsheet reader to load the file.

#### MS Excel

```text
=cmd|' /C notepad'!'A1'
```

#### LibreOffice Calc

```text
='file:///etc/passwd'#$passwd.A1
```

#### Step 2

Create a new page, injecting the correct formula, and export the pages as XLS.

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/python/Formula-Injection/7.png)

#### Step 3

Open the exported file in the spreadsheet app. After the interaction with the cell containing the injected formula, we can verify the command is executed.

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/python/Formula-Injection/8.png)

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/python/Formula-Injection/9.png)

What else can be done?

Check the Additional sources section below with more possibilities for Formula Injection!

## Additional sources

Please refer to the OWASP testing guide for a full complete description about Formula Injection \(CSV Injection\)!

{% embed url="https://owasp.org/www-community/attacks/CSV_Injection" %}

More references

{% embed url="https://payatu.com/csv-injection-basic-to-exploit" %}

{% embed url="https://www.contextis.com/us/blog/comma-separated-vulnerabilities" %}

{% embed url="https://pentestmag.com/formula-injection/" %}
