#!/usr/bin/env python

import os
import sys
from fabric.api import local, task
from fabric.context_managers import shell_env


@task
def backup():
    stop_docker_container()
    do_psql_dump()
    bup_init()
    bup_index()
    do_bup_backup()
    start_docker_container()


@task
def restore():
    do_bup_restore()


def do_bup_backup():
    print('Running incremental backup')
    backuped = local('BUP_DIR=$(pwd)/backup bup save -n crowdbackup $(pwd)')
    if backuped.return_code != 0:
        print 'An error occurred while backing up. Aborting...'
        sys.exit(1)


def do_bup_restore():
    restored = local('BUP_DIR=$(pwd)/backup bup restore -C crowdbackup '
                     'crowdbackup/latest/$(pwd)')
    if restored.return_code != 0:
        print 'An error occurred while restoring. Aborting...'
        sys.exit(1)


def bup_init():
    initiated = local('BUP_DIR=$(pwd)/backup bup init')
    if initiated.return_code != 0:
        print 'An error occurred while initiating bup. Aborting...'
        sys.exit(1)


def bup_index():
    indexed = local('BUP_DIR=$(pwd)/backup bup index --exclude-from '
                    '.bup.ignore $(pwd)')
    if indexed.return_code != 0:
        print 'An error occurred while indexing bup. Aborting...'
        sys.exit(1)


def do_psql_dump():
    print 'dumping...'
    dumped = local('docker run -t --rm --link crowd_database_1:db '
                   '-v $(pwd):/tmp postgres sh -c \'pg_dump -U crowd -h '
                   '"$DB_PORT_5432_TCP_ADDR" -w crowd > /tmp/crowd.dump\'')

    if dumped.return_code != 0:
        print 'An error occured while dumping database. Aborting...'
        sys.exit(1)
    print 'dumped...'


def stop_docker_container():
    print 'stoping...'
    stopped = local('sudo docker-compose stop crowd')
    if stopped.return_code != 0:
        print 'An error occurred while stoping container crowd. Aborting...'
        sys.exit(1)
    print 'stopped...'


def start_docker_container():
    print 'starting...'
    started = local('sudo docker-compose start crowd')
    if started.return_code != 0:
        print 'An error occurred while starting container crowd. Aborting...'
        sys.exit(1)
    print 'started...'
