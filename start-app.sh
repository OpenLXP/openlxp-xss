#!/usr/bin/env bash
# start-server.sh

python manage.py waitdb 
python manage.py migrate 
cd /opt/app/ 
if [ -n "$TMP_SCHEMA_DIR" ] ; then
    (cd openlxp-xss; install -d -o www-data -p $TMP_SCHEMA_DIR)
else
    (cd openlxp-xss; install -d -o www-data -p tmp/schemas)
fi
pwd 
service clamav-daemon restart
./start-server.sh