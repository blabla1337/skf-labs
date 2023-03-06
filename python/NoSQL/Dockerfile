### Static layers

FROM mongo:6.0.2 AS skf-mongo

# Installing needed binaries and deps. Then removing unneeded deps:
RUN apt update && apt install -y python3 python3-dev python3-pip dos2unix

### Dynamic layers
FROM skf-mongo

WORKDIR /home/app/NoSQL

COPY requirements.txt .

# Installing needed binaries and deps
RUN pip3 install --no-cache-dir  --user -r requirements.txt 

COPY . .

# Fixing Windows line endings for our students:
RUN find . -name "*.sh" -o -name "*.py" -o -name "*.css" -o -name "*.js" | xargs dos2unix

# Setting chmod +x on the scripts:
RUN find . -name "*.sh" -o -name "*.py" | xargs chmod +x

RUN ["chmod", "+x", "./entry.sh"]
ENTRYPOINT ["./entry.sh"]
