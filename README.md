# La Escupidera de Salty
## Stack
 1. Django 3.2.4
 2. python 3.6.13
 3. mysql  Ver 14.14 Distrib 5.7.33
 
## GETTING STARTED
### Create virtualenv
```
pip install virtualenv
virtualenv -p /path/to/python3.6 virtualenv
```
or
```
sudo apt install python3.6-venv
python3.6 -m venv /path/to/new/virtual/environment
virtualenv -p /path/to/python3.6 virtualenv
```
### Install requirements
```
pip install -r requirements/base.txt
```
### Create .env file
A _.env.example_ file can be found in *salty-spitoon/salty-spitoon/.env.example*. This files shows env variables to set for settings in order to run project. For tha purpose it was used [python-dotenv](https://pypi.org/project/python-dotenv/) package. Env file must be next to _settings.py_.
Fill variables with your own then, on **_salty-spitoon/salty-spitoon/_** folder, copy .env.example file
```
cp .env.example .env
```

### Database
Once you have defined database settings in _.env_ file, the you have to run django migrations. 
```
python salty-spitoon/manage.py migrate
```

### Users
In order to start testing the project, is necessary to create some users, this projects has fixtures files for that purpose. All users have the password **_escupideradesalty_**.
Inside *salty-spitoon* folder:
```
python manage.py loaddata fixtures/users.json
python manage.py loaddata fixtures/managerusers.json
```
Users have the following hierarchy:

 - boss@saltyspitoon.com
	 - manager1@saltyspitoon.com
		 - hitman1@saltyspitoon.com
		 - hitman2@saltyspitoon.com
		 - hitman3@saltyspitoon.com
	 - manager2@saltyspitoon.com
		 - hitman4@saltyspitoon.com
		 - hitman5@saltyspitoon.com
		 - hitman6@saltyspitoon.com
	 - manager3@saltyspitoon.com 
		 - hitman7@saltyspitoon.com
		 - hitman8@saltyspitoon.com
		 - hitman9@saltyspitoon.com

### Run project
Once you have finished previous steps you can run project on local environment.
``` python
python salty-spitoon/manage.py runserver 0.0.0.0:8000
```