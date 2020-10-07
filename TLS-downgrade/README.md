This is still a work-in-progress, a proof of concept without a write up.

The Docker build process is also a bit different, because this system isn't in Gitlab yet :D Hence why the Dockerfile is in here, instead of in the .\Docker directory.

Build instructions:
docker build -t skf-labs/tls-downgrade .
docker run -ti -p 5000:5000 skf-labs/tls-downgrade

