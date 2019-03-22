FROM ubuntu:latest
MAINTAINER Abhishek "abhiabhi2306@gmail.com"
RUN apt-get update -y && \ 
apt-get install -y python-dev build-essential python-pip
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]
