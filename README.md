# RedisOPM
Redis Operations Managerment

### 1.Create Project and APP
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


### 2.Run web service by Docker
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

#### Run Docker container by Docker-compose
```Bash
# docker-compose up -d
Creating network "djangocompose_NetRedis" with driver "bridge"
Creating djangocompose_django_1
# docker-compose ps
         Name                       Command               State           Ports          
----------------------------------------------------------------------------------------
djangocompose_django_1   python manage.py runserver ...   Up      0.0.0.0:8080->8000/tcp
```

Now, you can access the welcome page by browser !



