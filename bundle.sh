#!/bin/sh

# The purpose of this script is to bundle the application as a stand-alone zip
# archive which python can run. You can then move the file to a directory in
# your PATH, so that you can run the application directly from the command
# line.
#
# USAGE:
# cd /path/to/hunger/
# ./bundle.sh

prog_name="hunger"
src_dir=$(dirname $0)
appfiles="*.py mensa"

zip -r app.zip $appfiles --exclude .* __pycache__ *.pyc mensa/.* mensa/__pycache__ mensa/*.pyc mensa/scratchpad.py
echo '#!/usr/bin/env python3' | cat - app.zip > $prog_name
chmod +x $prog_name
rm app.zip
