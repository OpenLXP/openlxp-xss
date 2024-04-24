#!/usr/bin/env bash
# start-server.sh

python manage.py waitdb 
python manage.py migrate 
python manage.py loaddata admin_theme_data.json 
cd /tmp/app/ 
if [ -n "$TMP_SCHEMA_DIR" ] ; then
    (cd openlxp-xss; install -d -o 1001 -p $TMP_SCHEMA_DIR)
else
    (cd openlxp-xss; install -d -o 1001 -p tmp/schemas)
fi
pwd 
# service clamav-daemon restart
./start-server.sh