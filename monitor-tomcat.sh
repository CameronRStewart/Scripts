#!/bin/bash
# monitor-tomcat.sh: 

# Recommended cron:
# Cron description: Run every ten Minutes after 5 minutes past the hour.
#5,15,25,35,45,55 * * * * root /root/monitor-tomcat.sh

# Purpose: Monitor tomcat. If tomcat is not responding well, restart
#          both tomcat and apache.

MAILTO="libtech@unm.edu,jragle@unm.edu"
SERVICES=(httpd tomcat)
hostname=$(hostname --short)
TIME_WAIT="4m" #"1s" for testing
SUBJECT1="$hostname: web services restarted"
SUBJECT2="$hostname: web services not running!"
SUCCESS="HTTP/1.1 200 OK"
TRIMMED_SUCCESS=$(echo $SUCCESS | tr -d '[:space:]')
CURL=$(curl -Is "localhost" | head -n 1 | tr -d '[:space:]')

# Feature: Add a switch for silent/logging mode or manual, INFO mode.
#  For example the cron would run the silent mode only logging progress.
#  The other would assume manual run and output more [INFO] level output.

# Create a temp file to record the events of the session.
# This avoids having to manage logs this script will create via logrotate.d.
TMPFILE=$(mktemp -q /tmp/monitor-tomcat.cron.XXXXXX)
if [ $? -ne 0 ]; then
    echo "$0: Can not create temp file, exiting..."
    exit 1
fi

# Functions:

# time_date(): return the time/date right now.
time_date () { echo "$(date --rfc-3339=seconds)"; }

# get_status(): return the status code from a web connection.
get_status () { echo "$(curl -Is "localhost" | head -n 1 | tr -d '[:space:]')"; }

# get_minute (): return the current minute.
get_minute () { echo $(date +%M); }

# Main body of the script:

# Test for normal opperation
if [ "$(get_status)" == "$TRIMMED_SUCCESS" ]
then
    echo $(time_date) “[INFO] - $HOSTNAME: $SERVICES responded normally.” >> $TMPFILE;
    #DEBUG:     cat $TMPFILE;
    rm -f $TMPFILE;
    exit;
else
    # Assume something went wrong, stop services
    echo $(time_date) “[WARN] - $HOSTNAME: [$SERVICES] responded abnormally.” >> $TMPFILE;

    # Record how many CLOSE_WAIT connections 
    CLOSE_WAITS="$(cat /proc/net/tcp /proc/net/tcp6 2>/dev/null | awk ' /:/ { c[$4]++; } END { for (x in c) { print x, c[x]; } }' | tail -n 1 | cut -d ' ' -f 2)"
    echo $(time_date) "[WARN] - found $CLOSE_WAITS CLOSE_WAIT TCP connections." >> $TMPFILE;

    for item in ${SERVICES[*]}; do
        echo $(time_date) “[WARN] - $HOSTNAME:   Stopping $item” >> $TMPFILE;
        service $item stop &> /dev/null
        wait;
    done

    # Assume everything stopped cleanly, restart services
    for item in ${SERVICES[*]}; do
        echo $(time_date) “[WARN] - $HOSTNAME:   Starting $item” >> $TMPFILE;
        service $item start &> /dev/null
        wait;
    done

    # Consider putting a while loop to test for valid return code
    #  but also needs to timeout and give up after 5 minutes


    # WAIT for a spell before testing
    sleep $TIME_WAIT

    # Test web services again
    if [ "$(get_status)" == "$TRIMMED_SUCCESS" ]
    then
        echo $(time_date) “[WARN] - $HOSTNAME: [${SERVICES[*]}] have been restarted” >> $TMPFILE
        SUBJECT="$SUBJECT1";
    else
        echo $(time_date) “[ERROR] - $HOSTNAME: [${SERVICES[*]}] attempt to be restarted failed!!” >> $TMPFILE
        SUBJECT="$SUBJECT2";

    fi
fi

mail -s "$SUBJECT" $MAILTO < $TMPFILE;
#DEBUG cat $TMPFILE;
rm -f $TMPFILE;