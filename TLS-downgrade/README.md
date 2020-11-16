This is still a work-in-progress, a proof of concept without a write up.

The Docker build process is also a bit different, because this system isn't in the official Gitlab yet :D That's why there's two Dockerfiles: one to build from this dir, the other to pull from SKF Gitlab.

Build instructions:
cd TLS-downgrade
docker build -t skf-labs/tls-downgrade .
docker run -ti -p 5000:5000 --cap-add=NET_ADMIN skf-labs/tls-downgrade

How to work this container:
1. Start it normally and explore, based on the walkthrough. 
2. Start a shell inside the container and run ./start-interceptor.sh.
3. Testing from another host, for example:   openssl s_client -connect 10.0.0.50:5000 </dev/null
   With a browser should still work as well.
4. Stop the shell script and edit interceptor.py. On line 87 flip \x03 to \x01.
5. Restart the ./start-interceptor.sh script.
6. Test again with a browser: it'll fail. 
   Using some openssl clients will also fail, while others (like the one in the container) will fallback to TLS 1.0.
   
   