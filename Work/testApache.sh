#!/bin/bash                                                                                                                                                                                     \
                                                                                                                                                                                                 

email=""
hostname=""

DATE=$(date)

SUBJECT1="$hostname_httpd_has_been_restarted"
SUBJECT2="$hostname_httpd_is_not_running"
SUCCESS="HTTP/1.1 200 OK"
TRIMMED_SUCCESS=$(echo $SUCCESS | tr -d '[:space:]')

CURL=$(curl -Is "$hostname" | head -n 1 | tr -d '[:space:]')

if [ "$CURL" = "$TRIMMED_SUCCESS" ]
then
    echo $DATE “[INFO] - $hostname: httpd is running” >> /var/log/httpd/httpdmonitor.log
else
    /etc/init.d/httpd restart

    CURL_AGAIN=$(curl -Is "$hostname" | head -n 1 | tr -d '[:space:]')

    if [ "$CURL_AGAIN" = "$TRIMMED_SUCCESS" ]
    then
        echo $DATE “[WARN] - $hostname: httpd wasn’t running and has been started” >> /var/log/httpd/httpdmonitor.log | mail -s “$SUBJECT1” "$email"
    else
        echo $DATE “[ERROR] - $hostname: httpd was stopped and cannot be started!!!” >> /var/log/httpd/httpdmonitor.log | mail -s “$SUBJECT2” "$email"

    fi
fi