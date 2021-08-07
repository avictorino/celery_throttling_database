
# Throttling database connections in a distributed environment

![python_celery_redis_django_postgres](https://user-images.githubusercontent.com/1752695/128603659-c3602903-4d3f-4d03-8f26-6be91e1c715f.png)

### Objective:
Limit the database connections from a Cluster/Nodes auto-scalable.

This is a simple implementation to insert a reasonable amount of concurrent data using constraints and indexes in a controlled way.

To simulate the environment I create a web crawler to download a website data including the auto-referenced links and insert int the database.

Basically I splited the functionality into 3 concurrent tasks to be easy to throttle the execution however we want.

Set the rate limit for this task type (limits the number of tasks that can be run in a given time frame). 
Tasks will still complete when a rate limit is in effect, but it may take some time before it’s allowed to start.
    
    @celery_app.task(name="database_ingestor", rate_limit='10/s')
    
Example: “100/m” (hundred tasks a minute). This will enforce a minimum delay of 600ms between starting two tasks on the same worker instance.


### Database Result Backend
Keeping state in the database can be convenient for many, especially for web applications with a database already in place, but it also comes with limitations.
Polling the database for new states is expensive, and so you should increase the polling intervals of operations, such as result.get().
Some databases use a default transaction isolation level that isn’t suitable for polling tables for changes.


### Run Docker:

    $ docker-compose build
    $ docker-compose up

### Docker Compose.yml
Containe each worker required to start the process. Uncomment REDIS and Postgres if you don't already have them. 

   
### Database configurations
1 - Create a Postgres database named 'celery_ingestor'
    
2 - Create tables

    $ python manage.py migrate

Apply this command if you want to login into the admin panel:
    
    $ python manage.py createsuperuser   
    
![python_celery_redis_django_postgres](https://user-images.githubusercontent.com/1752695/128603676-f62eac13-7531-46ae-9051-643fa727e793.png)


After the docker containers are running open the following links to visualize the tasks and the database insertion:

    http://127.0.0.1:5002/tasks - Celery Dashboard
    http://127.0.0.1:8000/admin/core/page/ - Django admin 
    
    
To start the execution apply the following command line in the project root directory:
    ## !!! WARNING this script runs flushdb!!! 
    
    $python run.py 
    
### Tech Stack:
    Python
    Django
    Redis
    Celery
    Postgres
