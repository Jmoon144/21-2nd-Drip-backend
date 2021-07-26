import os

from .production import *

SECRET_KEY = os.environ['SECRET_KEY']
ALGORITHM = os.environ['ALGORITHM']
SECRET_ACCESS_KEY = os.environ['SECRET_ACCESS_KEY']
DATABASES = os.envior['DATABASE']
DEBUG = True