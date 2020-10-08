This is still a work-in-progress, a proof of concept without a write up.

The Docker build process is also a bit different, because this system isn't in Gitlab yet :D Hence why the Dockerfile is in here, instead of in the .\Docker directory.

Build instructions:
docker build -t skf-labs/tls-downgrade .
docker run -ti -p 5000:5000 --cap-add=NET_ADMIN skf-labs/tls-downgrade

Testing from another host, for example:
openssl s_client -connect 10.0.0.50:5000 -cipher ECDHE-RSA-AES256-SHA -tls1 </dev/null
openssl s_client -connect 10.0.0.50:5000 -cipher ECDHE-RSA-AES256-SHA -tls1_2 </dev/null

I've picked ECDHE-RSA-AES256-SHA because, with OpenSSL on Kali Linux, that's the cipher both TLS 1.2, 1.0 and SSLv3 have in common. Our client and server consider that one valid for all three standards.

