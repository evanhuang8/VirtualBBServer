from fabric.api import *

def dev():
  local('python manage.py runserver 0.0.0.0:8080')

def test():
  local('python manage.py test snapshot')