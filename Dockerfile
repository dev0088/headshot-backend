# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.6

ARG DATABASE_ENGINE
ARG DATABASE_NAME
ARG DATABASE_USER_NAME
ARG DATABASE_PASSWORD
ARG DATABASE_HOST
ARG DATABASE_PORT

ENV DATABASE_ENGINE=${DATABASE_ENGINE}
ENV DATABASE_NAME=${DATABASE_NAME}
ENV DATABASE_USER_NAME=${DATABASE_USER_NAME}
ENV DATABASE_PASSWORD=${DATABASE_PASSWORD}
ENV DATABASE_HOST=${DATABASE_HOST}
ENV DATABASE_PORT=${DATABASE_PORT}
ENV PYTHONUNBUFFERED 1

# Setup Ubuntu linux
RUN export LANGUAGE="en_US.UTF-8"
RUN apt-get update && apt-get install -y --no-install-recommends
RUN apt-get -y install build-essential curl libssl-dev libffi-dev zlib1g-dev libjpeg-dev checkinstall python3-pythonmagick inkscape xvfb poppler-utils libfile-mimeinfo-perl qpdf libimage-exiftool-perl
RUN apt-get install imagemagick
# RUN echo Y | apt-get install gdal-bin
RUN apt-get -y install binutils libproj-dev gdal-bin
# RUN add-apt-repository ppa:libreoffice/ppa
RUN apt-get update
RUN apt-get -y install libreoffice
RUN apt-get -y install postgresql-contrib

##############################################
# RUN apt-get install python3-dev
# RUN apt-get install python3-pip
# RUN sudo apt-get install python3-venv
# RUN python3.6 -m venv env3
# RUN source env3/bin/activate
# RUN nano /etc/systemd/system/uwsgi.service
##############################################

# Exiftool
# RUN wget https://sno.phy.queensu.ca/~phil/exiftool/Image-ExifTool-11.11.tar.gz
# RUN mkdir -p /usr/src/image_exiftool
# RUN tar -zxvf Image-ExifTool-11.11.tar.gz -C /usr/src/image_exiftool
# RUN rm Image-ExifTool-11.11.tar.gz
# # RUN gzip -dc Image-ExifTool-11.11.tar.gz | tar -xf -
# RUN cd /usr/src/image_exiftool
# RUN pwd
# RUN ls /usr/src/image_exiftool
# RUN perl Makefile.PL
# RUN make install

RUN mkdir -p /usr/src/headshot_backend

WORKDIR /usr/src/headshot_backend
RUN mkdir -p /usr/src/headshot_backend/run

COPY requirements.txt /usr/src/headshot_backend/

RUN pip install -r /usr/src/headshot_backend/requirements.txt 

RUN mkdir -p /usr/src/headshot_backend/static_backend
RUN mkdir -p /usr/src/headshot_backend/static_backend/js
RUN mkdir -p /usr/src/headshot_backend/static_backend/css
RUN mkdir -p /usr/src/headshot_backend/static_backend/fonts
RUN mkdir -p /usr/src/headshot_backend/static_backend/images
RUN mkdir -p /usr/src/headshot_backend/static_backend/rest_framework
RUN mkdir -p /usr/src/headshot_backend/static_backend/rest_framework_swagger

COPY . /usr/src/headshot_backend/

# RUN ls /usr/src/headshot_backend

RUN python /usr/src/headshot_backend/manage.py collectstatic --noinput
# RUN python manage.py makemigrations 
# RUN python manage.py migrate

EXPOSE 8000

# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["./start.sh"]