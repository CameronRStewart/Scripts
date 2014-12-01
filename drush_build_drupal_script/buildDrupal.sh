#!/bin/bash

####################################
#
#	This script downloads drupal and specified modules, sets up the site and
#	optionally imports a database dump.  Variables may be passed in, set 
#	directly in the first section of this file, or included via a separate file
#	in the same directory named 'config.conf'.
#
# OPTIONS
#
# d	Directory to download install Drupal into:  this directory will be created
#		under /var/www/html/webenv  (DNAME)
# f	Path to SQL dump file, used to restore/move database  (FNAME)
# u	MySQL database username  (DBUSER)
# p	MySQL database password  (DBPASS)
# n	MySQL database name  (DBNAME)
# a	Drupal site admin password  (ADMINPASS)
# c	Path to files directory to copy over installed files  (FILESDIR)
# l	Path to libraries directory to copy over installed libraries  (LIBRARIESDIR)
# m	Module list to download (DLMOD)
# e	Module list to enable (ENMOD)
#
####################################

DNAME=
FNAME=
DBUSER=
DBPASS=
DBNAME=
ADMINPASS=
FILESDIR=
LIBRARIESDIR=
DLMOD=""
ENMOD=""

# get file with variables defined
#if [ -f config.conf ];
#then
#	source config.conf
#fi

# get options, set variables; if variable values supplied above,
# simply do not use options
while getopts "d:u:p:n:a:f:c:l:" opt; do
  case $opt in
    d)
      DNAME=$OPTARG
      ;;
    f)
      FNAME=$OPTARG
      ;;
    u)
      DBUSER=$OPTARG
      ;;
    p)
      DBPASS=$OPTARG
      ;;
    n)
      DBNAME=$OPTARG
      ;;
    a)
      ADMINPASS=$OPTARG
      ;;
    c)
      FILESDIR=$OPTARG
      ;;
    l)
      LIBRARIESDIR=$OPTARGS
      ;;
    m)
      DLMOD=$OPTARGS
      ;;
    e)
      ENMOD=$OPTARGS
      ;;
  esac
done

# make sure database variables are set
if [ ! -n "$DBUSER" ]
  then DBUSER=ibservicesuser
fi
if [ ! -n "$DBPASS" ]
  then DBPASS=ibservicespasswd
fi
if [ ! -n "$DBNAME" ]
  then DBNAME=ibservicesdata
fi
if [ ! -n "$ADMINPASS" ]
  then ADMINPASS=pples4u
fi

# create directory for files and cd into it
mkdir "/var/www/html/webenv/$DNAME"
cd "/var/www/html/webenv/$DNAME"

# download and set up drupal
drush dl drupal

# make .files move with cp *
shopt -s dotglob

# move drupal files up one directory
for entry in "/var/www/html/webenv/$DNAME"/*
do
  mv "$entry"/* "/var/www/html/webenv/$DNAME"
  rm -Rf "$entry"
done

drush si -y --db-url=mysql://"$DBUSER":"$DBPASS"@localhost:3306/"$DBNAME" --account-pass="$ADMINPASS"

# set timezone
drush vset date_default_timezone "America/Denver"

# Set default country
drush vset site_default_country 'US'

# Set first day of week
# 0 = Sunday, 1 = Monday, ...
drush vset date_fist_day 1

drush vset date_api_use_iso8601 0 -y

# download and enable modules

drush dl "$DLMOD" -y
drush en "$ENMOD" -y

# update everything
drush pm-update

# create our typical custom directories
printf "Creating custom directories.\n\n"
mkdir "/var/www/html/webenv/$DNAME/sites/all/backups"
mkdir "/var/www/html/webenv/$DNAME/sites/all/libraries"
mkdir "/var/www/html/webenv/$DNAME/sites/all/temp"

# copy files directory if specified
if [ -n "$FILESDIR" ]
then 
printf "Copying 'files' directory\n\n"
'cp' -R "$FILESDIR" "/var/www/html/webenv/$DNAME/sites/default"
fi

# copy libraries directory if specified
if [ -n "$LIBRARIESDIR" ]
then 
printf "Copying 'files' directory\n\n"
'cp' -R "$LIBRARIESDIR" "/var/www/html/webenv/$DNAME/sites/all"
fi


# update ownership for whole directory structure and permissions on files directory
printf "Updating ownership for /var/www/html/webenv/$DNAME\n\n"
chown -R root.apache "/var/www/html/webenv/$DNAME"
printf "Updating file/directory permissions\n\n"

find /var/www/html/webenv/"$DNAME"/sites/default/files -type d -exec chmod 775 '{}' \;
find /var/www/html/webenv/"$DNAME"/sites/default/files -type f -exec chmod 644 '{}' \;

chmod 755 "/var/www/html/webenv/$DNAME/sites/default/files"

chmod -R 755 "/var/www/html/webenv/$DNAME/sites/default"

chmod -R 444 "/var/www/html/webenv/$DNAME/sites/default/settings.php"


# restore db if present
if [ -n "$FNAME" ]
then 
printf "Restoring database.\n\n"
drush sql-query --file="$FNAME"
fi

# clear caches
printf "Clearing all Drupal caches\n\n"
drush cc all

# restart httpd
printf "Restarting Apache Web Server\n\n"
service httpd restart

# run drush status report for site
drush status

