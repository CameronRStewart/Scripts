#!/bin/bash

# Recommended cron:
# Cron description: Run every ten Minutes after 5 minutes past the hour.
#5,15,25,35,45,55 * * * * root /root/monitor-tomcat.sh

# Purpose: Monitor tomcat. If tomcat is not responding well, restart
#          both tomcat and apache.

MAILTO="libtech@unm.edu"
SERVICES=(httpd tomcat)
hostname=$(hostname --short)
TIME_WAIT="1m" #"1s" for testing
DATE=$(date)
SUBJECT1="$hostname: web services restarted"
SUBJECT2="$hostname: web services not running!"
SUCCESS="HTTP/1.1 200 OK"
TRIMMED_SUCCESS=$(echo $SUCCESS | tr -d '[:space:]')
CURL=$(curl -Is "localhost" | head -n 1 | tr -d '[:space:]')

# Create a temp file to record the events of the session.
# This avoids having to manage logs this script will create via logrotate.d.
TMPFILE=$(mktemp -q /tmp/monitor-tomcat.cron.XXXXXX)
if [ $? -ne 0 ]; then
    echo "$0: Can not create temp file, exiting..."
    exit 1
fi

# Test for normal opperation
if [ "$CURL" = "$TRIMMED_SUCCESS" ]
then
    echo $DATE “[INFO] - $HOSTNAME: $SERVICES responded normally.” >> $TMPFILE;
    #DEBUG: cat $TMPFILE;
    rm -f $TMPFILE;
    exit;
else
    # Assume something went wrong, stop services
    echo $DATE “[WARN] - $HOSTNAME: [$SERVICES] responded abnormally.” >> $TMPFILE;
    for item in ${SERVICES[*]}; do
        echo $DATE “[WARN] - $HOSTNAME:   Stopping $item” >> $TMPFILE;
        service $item stop
    done

    # Assume everything stopped cleanly, restart services
    for item in ${SERVICES[*]}; do
        echo $DATE “[WARN] - $HOSTNAME:   Starting $item” >> $TMPFILE;
        service $item start
    done

    # WAIT for a spell before testing
    sleep $TIME_WAIT

    CURL_AGAIN=$(curl -Is "localhost" | head -n 1 | tr -d '[:space:]')

    if [ "$CURL_AGAIN" = "$TRIMMED_SUCCESS" ]
    then
        echo $DATE “[WARN] - $HOSTNAME: [$SERVICES] have been restarted” >> $TMPFILE
        SUBJECT=$SUBJECT1;
    else
        echo $DATE “[ERROR] - $HOSTNAME: [$SERVICES] attempt to be restarted failed!!” >> $TMPFILE
        SUBJECT=$SUBJECT2;

    fi
fi

mail -s $SUBJECT $MAILTO < $TMPFILE;
cat $TMPFILE;  # This will end up in cron logs
rm -f $TMPFILE;