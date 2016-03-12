# Django for IoT

Created from https://github.com/heroku/heroku-django-template/

## LIFX setup

LIFX_TOKEN: get from https://cloud.lifx.com/


## Run locally

```
export LIFX_TOKEN=mytoken
export DATABASE_URL=postgres://localhost/mydbname
createdb mydbname
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

log into localhost:8000/admin

click on Device and add a device

or in a python terminal:

```
from apps.lifx import client
client.configure_devices()
```

## Deployment to Heroku

    $ git init
    $ git add -A
    $ git commit -m "Initial commit"

    $ heroku create
    $ git push heroku master

    $ heroku run python manage.py migrate


to use management commands:
```

```


## Ways to interact with devices

* POST to views
* run management commands
* run celery periodic tasks



## Design decisions / gotchas

* where to put db indexes
	* Observation.valid_at
* pass device or device_pk to tasks
* just Observation model, or Observation and DataSet
* structure Observation list to work with graphing package of choice
* paginate Observation list view
* different settings files
	* local, heroku with scheduler, heroku with celery
* set_status, etc views on devices or interactions
* POST to do interaction
* security features
* mock tests
* add LIFX to new wifi: https://support.lifx.com/hc/en-us/articles/204318224