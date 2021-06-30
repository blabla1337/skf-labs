# KBID 3 - Cross site scripting \(attribute\)

## Running the app Docker

```text
$ sudo docker pull blabla1337/owasp-skf-lab:xss-attribute
```

```text
$ sudo docker run -ti -p 127.0.0.1:5000:5000 blabla1337/owasp-skf-lab:xss-attribute
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

### Step 1

The application shows an input fields that allows the user to change the color of the text shown in the page.

![](.gitbook/assets/xss-attribute-1.png)

If we want to make it red, we can just write `red` in the input box and click the Submit Button.

![](.gitbook/assets/xss-attribute-2.png)

```markup
<center> <p style="font-size:2em;"> {% autoescape false %}<span style='color:{{xss}};' > Let me be a new color!</span>{% endautoescape %}</p></center>
```

and it is not escaped so it should be possible to perform a Cross Site Scripting \(XSS\) injection.

## Exploitation

### Step 1

Now we have seen where the user input is being reflected in the style, we will have to look what dangerous HTML characters are not properly escaped, when the developer used the right encoding the metacharacters like " >< will be properly encoded. So we need to form a payload that does not utilize these characters in order to make the attack successful like the following payload:

*note: we disabled auto-escape for the challenge but in order to do it well you need to avoid using the " > < to leverage the attack*


```text
red ' onmouseover='alert(1337)'
```

Now, hovering over the paragraph will trigger our javascript event handler!

![](.gitbook/assets/xss-attribute-4.png)

## Mitigation
XSS Prevention Rules:
The following rules are intended to prevent all XSS in your application. While these rules do not allow absolute freedom in putting untrusted data into an HTML document, they should cover the vast majority of common use cases.
RULE #0 - Never Insert Untrusted Data Except in Allowed Locations
RULE #1 - HTML Encode Before Inserting Untrusted Data into HTML Element Content
RULE #2 - Attribute Encode Before Inserting Untrusted Data into HTML Common Attributes
RULE #3 - JavaScript Encode Before Inserting Untrusted Data into JavaScript Data Values
RULE #4 - CSS Encode And Strictly Validate Before Inserting Untrusted Data into HTML Style Property Values
RULE #5 - URL Encode Before Inserting Untrusted Data into HTML URL Parameter Values
RULE #6 - Sanitize HTML Markup with a Library Designed for the Job
RULE #7 - Avoid JavaScript URLs
RULE #8 - Prevent DOM-based XSS

In this case, the input is directly rendered into the application without without following above rules so that the attacker can inject a malicious script.\
In the following vulnerable code, as there isn't any form of validation an attacker can manipulate the inputs.

Here the vulnerable code is:
![](.gitbook/assets/xssurlold.png)

For the fix, we have implemented URL validation by using validators package
![](.gitbook/assets/xssurlnew.png)




## Additional sources

Please refer to the OWASP testing guide for a full complete description about path traversal with all the edge cases over different platforms!

{% embed url="https://www.owasp.org/index.php/Testing\_for\_Reflected\_Cross\_site\_scripting\_\(OTG-INPVAL-001\)" caption="" %}
