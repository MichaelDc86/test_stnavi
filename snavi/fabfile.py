from fabric.api import local


def rs():
    local('python manage.py runserver')


def mm():
    local('python manage.py makemigrations')


def m():
    local('python manage.py migrate')
