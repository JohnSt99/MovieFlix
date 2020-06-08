FROM ubuntu:16.04 
MAINTAINER John St <e17144@unipi.gr - jsm@hotmail.gr>
RUN apt-get update
RUN apt-get install -y python3 python3-pip 
RUN pip3 install flask pymongo 
COPY requirements.txt /requirements/requirements.txt
RUN pip3 install -r requirements/requirements.txt
RUN mkdir /app
RUN mkdir -p /app/data
COPY service.py /app/service.py  
COPY templates /app/templates
ADD data /app/data 
WORKDIR /app
ENTRYPOINT [ "python3","-u", "service.py" ]
