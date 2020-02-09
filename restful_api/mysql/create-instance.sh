#! /usr/bin/env bash

wait_for_line () {
    while read line
    do
        echo "$line" | grep -q "$1" && break
    done < "$2"
    # Read the fifo for ever otherwise process would block
    cat "$2" >/dev/null &
}

# Start Temperory MySQL process
MYSQL_DATA="/tmp/mysql-toxusage"
mkdir -p ${MYSQL_DATA} && mysqld --initialize --datadir=${MYSQL_DATA} && mkfifo ${MYSQL_DATA}/out
mysqld --datadir=${MYSQL_DATA} \
    --pid-file=${MYSQL_DATA}/mysql.pid \
    --socket=${MYSQL_DATA}/mysql.socket \
    --skip-networking \
    --skip-grant-tables \
    --skip-networking \
    &> ${MYSQL_DATA}/out &

# Wait for MySQL to start listening to connections
wait_for_line "mysqld: ready for connections." ${MYSQL_DATA}/out
SOCKET_FILE="${MYSQL_DATA}/mysql.socket"

# create database testdb
SQL_FILE=${MYSQL_DATA}/createdb.sql
echo "CREATE DATABASE TESTDB DEFAULT CHARACTER SET UTF8MB4 COLLATE UTF8MB4_UNICODE_CI" > ${SQL_FILE}
mysql --socket=${SOCKET_FILE} < ${SQL_FILE} && echo "database testdb created"

# echo result
echo "testing mysql ready for use: socket file at ${SOCKET_FILE}"
