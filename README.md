# RedisOPM
Redis Operations Managerment

### Run a django contianer
Create a Django docker-compose.yml in /data/RedisOPM/Docker/Django_compose .

1. First, run the below command to create project, it will create the manage.py and mysite directory.
```
# docker run -it --rm -v /data/RedisOPM/WebMM:/code -w /code django django-admin.py startproject mysite .
```
> If you had not create manage.py , you will get the error:
```
# docker-compose up 
Creating network "djangocompose_NetRedis" with driver "bridge"
Creating djangocompose_django_1
Attaching to djangocompose_django_1
django_1  | python: can't open file 'manage.py': [Errno 2] No such file or directory
djangocompose_django_1 exited with code 2
```


