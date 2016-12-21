# RedisOPM
Redis Operations Managerment

### Create Project and APP
#### Create Django Project
First, run the below command to create project, it will create the manage.py and mysite directory.
```Bash
# docker run -it --rm -v /data/RedisOPM/WebMM:/code -w /code django django-admin.py startproject mysite .
```

#### Create Django APP
Then, create the app directory.
```Bash
# docker run -it --rm -v /data/RedisOPM/WebMM:/code -w /code django python manage.py startapp RedisWebapp
```


### Run a django contianer
#### Create docker-compose.yml
Create a Django docker-compose.yml in /data/RedisOPM/Docker/Django_compose .
> docker-compose.yml
```Bash
version: '2'
services:
    django:
        image: django
        volumes: 
             - /data/RedisOPM/WebMM:/code
        ports:
             - 8080:8000
        networks:
             - NetRedis
        working_dir: /code
        command: python manage.py runserver 0.0.0.0:8000
networks:
    NetRedis:
        driver: bridge
        ipam:
            config:
                - subnet: 10.0.0.0/24
                  ip_range: 10.0.0.0/24
                  gateway: 10.0.0.1
```


