Python/Django + JWT auth backend
================================

### Technical Stack

	- Python/Django: python 3.6,

	- Database: PostgreSQL

	- JWT auth based RESTful API

### Create server

	```
	$ python3.6 -m venv env3

	$ source env3/bin/activate

	$ pip install coreapi django djangorestframework djangorestframework-jwt

	$ pip freeze > requirements.txt

	$ django-admin startproject config .
	```

### Get static files

	```
	$ ./manage.py collectstatic
	```

### Migrate models into database
	```
	$ ./manage.py makemigrations
	```

### Create admin user on server

	```
	$ ./manage.py migrate

	$ ./manage.py createsuperuser
	```

### Pre-requirement

	1. Install GDAL library for GeoIP/GeoLocation support

	- MacOS
		```
		$ brew install postgis
		$ brew install gdal
		$ brew install libgeoip
		```

	- Ubuntu
		```
		$ sudo apt-get install binutils libproj-dev gdal-bin
		```

### Run server
	```
	$ ./manage.py runserver
	```

### Server urls

- http://127.0.0.1:8000

- http://127.0.0.1:8000/api/auth/token/obtain/

- http://127.0.0.1:8000/api/echo
