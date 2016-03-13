from .common import *

SECRET_KEY = os.environ.get('SECRET_KEY')

# use CloudAMQP if using celery
BROKER_URL = os.environ.get('CLOUDAMQP_URL', None)
