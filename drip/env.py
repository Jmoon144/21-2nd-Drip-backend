import os

from .production import *

SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = os.environ.get('ALGORITHM')
SECRET_ACCESS_KEY = os.environ.get('SECRET_ACCESS_KEY')
DATABASES = os.environ.get('DATABASE')
DEBUG = True