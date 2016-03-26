from celery.schedules import crontab

SCHEDULE = {
    'refresh_all': {
        'task': 'django_iot.apps.interactions.tasks.refresh_all',
        'schedule': crontab(minute='*/5')
    },
    'vote_red': {
        'task': 'django_iot.apps.interactions.tasks.run_twitter_vote',
        'schedule': crontab(minute='*/5'),
        'kwargs': {
            'device_id': 1,
            'hashtag': '#red',
        }
    },
}
