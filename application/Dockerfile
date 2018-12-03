FROM fsadykov/centos_python
MAINTAINER Farkhod Sadykov
EXPOSE 5000 80 443
COPY . /root
WORKDIR /root
RUN python3.6 -m pip install --upgrade pip
RUN python3.6 -m pip install -r requirements.txt
WORKDIR /app
CMD ["python3.6", "app.py"]
