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
```
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



### Troubleshooting

- Remove all migrations
```
	$ find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
	$ find . -path "*/migrations/*.pyc"  -delete
```