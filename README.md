Python/Django + JWT auth backend
================================

### Technical Stack

	- Python/Django: python 3.6,

	- Database: PostgreSQL

	- JWT auth based RESTful API

### Setup environments

	1. Install python3.6 

	2. Install virtual environment for python3.6

	```
	$ python3.6 -m venv env3

	$ source env3/bin/activate

	$ pip install -r requirements.txt
  ```
	
### Get static files

	```
	$ mkdir static_backend/js
	
	$ mkdir static_backend/css

	$ mkdir static_backend/fonts

	$ mkdir static_backend/images

	$ ./manage.py collectstatic
	```

### Create database on db tool

- create `headshot` database on db tool such as `pgAdmin` or `TablePlus`

### Migrate models into database
	```
	$ ./manage.py makemigrations
	```

### Create tables with migration files and create admin user on server

	```
	$ ./manage.py migrate

	$ ./manage.py createsuperuser
	```

### Run server with command line
	```
	$ ./manage.py runserver 0.0.0.0:8000
	```

### Server urls

- admin page: http://localhost:8000/admin

- api page: http://localhost:8000/apis


### Add productions and quentities for each productions on admin page

- add more productions than 2
- add more quentities than 3

### Deploy server with Docker

- Run these commands on production server

```
$ docker stop headshot-backend
$ echo y | docker container prune
$ echo y | docker image prune

$ docker pull valeriia333/headshot-backend

$ docker network create --subnet=172.17.0.0/16 headshotnet

$ docker run -d \
	-e DATABASE_ENGINE=django.db.backends.postgresql_psycopg2 \
	-e DATABASE_NAME=headshot \
	-e DATABASE_USER_NAME=postgres \
	-e DATABASE_PASSWORD=postgres \
	-e DATABASE_HOST=206.189.193.17 \
	-e DATABASE_PORT=5432 \
	-p 8000:8000 \
	--net headshotnet \
	--ip 172.20.0.2 \
	--name headshot-backend \
	valeriia333/headshot-backend
```

- Run docker from docker hub on local
```
$ docker run -d \
	-e DATABASE_ENGINE=django.db.backends.postgresql_psycopg2 \
	-e DATABASE_NAME=headshot \
	-e DATABASE_USER_NAME=postgres \
	-e DATABASE_PASSWORD=postgres \
	-e DATABASE_HOST=192.168.0.121 \
	-e DATABASE_PORT=5432 \
	-p 8000:8000 \
	--name headshot-backend \
	valeriia333/headshot-backend
```

- Build docker and run it on local

```
$ docker build . -t headshot-backend

$ docker run -d \
	-e DATABASE_ENGINE=django.db.backends.postgresql_psycopg2 \
	-e DATABASE_NAME=headshot \
	-e DATABASE_USER_NAME=postgres \
	-e DATABASE_PASSWORD=postgres \
	-e DATABASE_HOST=192.168.0.121 \
	-e DATABASE_PORT=5432 \
	-p 8000:8000 \
	--name headshot-backend \
	headshot-backend

If you want to stop docker and rebuild / restart it, run these commands.

$ docker stop headshot-backend
$ docker rm headshot-backend
$ echo y | docker container prune
$ echo y | docker image prune

run above commands for building and running 

```

### Troubleshooting

- Remove all migrations
```
	$ find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
	$ find . -path "*/migrations/*.pyc"  -delete
```

### Additional 

- Rendering doc file to image for preview-generate package
```
	$ brew upgrade glibmm
	$ brew cask install xquartz
	$ brew cask install inkscape
	$ brew install xorg-server
	$ ln -s /opt/local/bin/inkscape /Applications/Inkscape
	$ brew install unoconv

	In the case Mac OS, 

	$ brew install freetype 
	$ brew install imagemagick
	$ brew install libmagic
	$ brew install ghostscript

	$ brew install imagemagick@6
	$ ln -s /usr/local/Cellar/imagemagick@6/6.9.10-9/lib/libMagickWand-6.Q16.dylib /usr/local/lib/libMagickWand.dylib

	In the case Ubuntu,
	$ apt-get install zlib1g-dev libjpeg-dev

	In the case CentOS
	$ yum install zlib1g-dev libjpeg-dev
```