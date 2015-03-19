## Atlassian crowd

For more information on the app please refere to the offical
Atlassian websites:


- [crowd](https://www.atlassian.com/software/crowd)

### Prerequisites

TBD

### Deploy/Update the application

    # rebuild the docker images
    $ docker-compose build

    # restart the docker images
    $ docker-compose up -d

    # inspect the logs
    $ docker-compose logs

If you deploy the app for the first time you may need to restore the database
from a backup for each app and adapt the database connection settings!

### Debug (aka. go inside) an image

    # execute a bash shell
    $ docker exec -it crowd_crowd_1 bash

### First run

If you start this orchestration for the first time, a handy feature is to
import your old data. If you're e.g. moving everything to another server
you can put your database backups into the tmp folder and the db initscript
will pick them up automagically on the first run.

    # move your crowd db backup file to tmp (filename is important).
    $ mv crowd.dump tmp/crowd.dump

    # unpack your crowd-home backup archive
    $ tar xzf crowd-home.tgz --strip=1 -C home

### Backup the home folders

    $ mkdir -p backup/$(date +%F)
      tar czf backup/$(date +%F)/crowd-home.tgz home

### Backup the PostgreSQL data

    # backup the crowd database
    $ docker run -it --rm --link atlassian_database_1:db -v $(pwd):/tmp \
        postgres sh -c 'pg_dump -U crowd -h "$DB_PORT_5432_TCP_ADDR" \
        -w crowd > /tmp/crowd.dump'

### Restore the PostgreSQL data

    # restore the crowd database backup
    $ docker run -it --rm --link atlassian_database_1:db -v $(pwd):/tmp \
        postgres sh -c 'pg_restore -U crowd -h "$DB_PORT_5432_TCP_ADDR" \
        -n public -w -d crowd /tmp/crowd.dump'
