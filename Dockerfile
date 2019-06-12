FROM ubuntu:18.04
COPY . /user_crud
WORKDIR /user_crud
RUN apt-get update \
    && apt-get -y install python3-pip \
	&& pip3 install -U flask-cors \
	&& pip3 install flask-mysql \
	&& apt-get -y install libmysqlclient-dev \
	&& pip3 install mysqlclient \
	&& pip3 install PyMySQL
EXPOSE 5000
ENTRYPOINT ["python3"]
CMD ["main.py"]