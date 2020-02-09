#! /usr/bin/env bash

pkill -F ${1}/mysql.pid  && echo "mysql testing process killed" || echo "doesnt kill anything"
