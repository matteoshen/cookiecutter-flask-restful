#! /usr/bin/env bash

pkill -F /tmp/mysql-toxusage/mysql.pid  && echo "mysql testing process killed" || echo "doesnt kill anything"
