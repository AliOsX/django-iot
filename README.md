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
from django_iot.apps.lifx import client
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
heroku addons:create scheduler:standard
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
* add LIFX to new wifi: reset (https://support.lifx.com/hc/en-us/articles/200468240-Hardware-Resetting-LIFX-Bulbs), add to wifi, then claim (https://support.lifx.com/hc/en-us/articles/203711234-Connecting-your-LIFX-to-the-Cloud)
* import celery into __init__
* schedule as own module
* can't make schedule depend on database (if not using djcelery)
* worker/scheduler dyno sleeps on free level!


celery resources:
* https://www.cloudamqp.com/docs/celery.html
* https://library.launchkit.io/three-quick-tips-from-two-years-with-celery-c05ff9d7f9eb#.e3a9mgoud
* https://realpython.com/blog/python/asynchronous-tasks-with-django-and-celery/
* https://devcenter.heroku.com/articles/celery-heroku#celery-and-django
