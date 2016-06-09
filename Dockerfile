FROM docteurfraise/flask-python34
RUN apt-get update
RUN apt-get install -y python-pip
RUN apt-get install -y mongodb-clients
RUN pip install pymongo
