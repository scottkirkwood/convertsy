#!/bin/bash
#
# Author: scottakirkwood@gmail.com (Scott Kirkwood)

# cd to the scripts folder
cd "$(dirname $0)"

# Output the app version number
echo -n 'App version is: '
grep '^version: .*' app.yaml

read -p "Is this correct? (enter to continue, ctrl-c to quit)"

# Upload everything
~/bin/google_appengine/appcfg.py --email=scottakirkwood@gmail.com update .
