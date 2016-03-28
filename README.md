# Django for IoT

This is the demo to accompany my talk on [Django for IoT](https://djangocon.eu/speakers/9) at DjangoCon Europe 2016.
It controls an LIFX light bulb based on Twitter voting.

You can fork this to play around with your own projects, or get started fresh with https://github.com/aschn/cookiecutter-django-iot

# Get started

## LIFX setup

LIFX_TOKEN: get from https://cloud.lifx.com/


## Twitter setup

Sign into https://apps.twitter.com/ with your twitter account, and click "create new app"


## Run locally

```
export DATABASE_URL=postgres://localhost/mydbname
export LIFX_TOKEN=[your value]
export TWITTER_CONSUMER_KEY=[your value]
export TWITTER_CONSUMER_SECRET=[your value]
export TWITTER_ACCESS_TOKEN=[your value]
export TWITTER_ACCESS_SECRET=[your value]
export VOTE_HASHTAG=[your hashtag]
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


celery resources:
* https://www.cloudamqp.com/docs/celery.html
* https://library.launchkit.io/three-quick-tips-from-two-years-with-celery-c05ff9d7f9eb#.e3a9mgoud
* https://realpython.com/blog/python/asynchronous-tasks-with-django-and-celery/
* https://devcenter.heroku.com/articles/celery-heroku#celery-and-django
