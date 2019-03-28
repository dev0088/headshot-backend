# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.6

ENV PYTHONUNBUFFERED 1

# Setup Ubuntu linux
RUN export LANGUAGE="en_US.UTF-8"
RUN apt-get update 
RUN apt-get -y install build-essential curl libssl-dev libffi-dev zlib1g-dev libjpeg-dev checkinstall
RUN apt-get install imagemagick
RUN sudo apt-get install binutils libproj-dev gdal-bin

RUN add-apt-repository ppa:libreoffice/ppa
RUN apt-get update
RUN apt-get install libreoffice

RUN apt-get install python3-dev
RUN apt-get install python3-pip
# RUN sudo apt-get install python3-venv
# RUN python3.6 -m venv env3
# RUN source env3/bin/activate

# RUN nano /etc/systemd/system/uwsgi.service

RUN mkdir -p /usr/src/headshot_backend

WORKDIR /usr/src/headshot_backend
RUN mkdir -p /usr/src/headshot_backend/run

COPY requirements.txt /usr/src/headshot_backend/

RUN pip install -r /usr/src/headshot_backend/requirements.txt 

COPY . /usr/src/headshot_backend/

RUN mkdir -p /usr/src/headshot_backend/static_backend
RUN mkdir -p /usr/src/headshot_backend/static_backend/js
RUN mkdir -p /usr/src/headshot_backend/static_backend/css
RUN mkdir -p /usr/src/headshot_backend/static_backend/fonts
RUN mkdir -p /usr/src/headshot_backend/static_backend/images
RUN mkdir -p /usr/src/headshot_backend/static_backend/rest_framework
RUN mkdir -p /usr/src/headshot_backend/static_backend/rest_framework_swagger
RUN ls /usr/src/headshot_backend 

RUN python /usr/src/headshot_backend/manage.py collectstatic --noinput
RUN python /usr/src/headshot_backend/manage.py makemigrations 
RUN python /usr/src/headshot_backend/manage.py migrate

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]