#!/bin/bash

cd /home/th/Code/Python/Django/retouches_dev/retouches.code/
tar --exclude='__pycache__'\
    --exclude='migrations'\
    -cvzf ../retouches.tar.gz\
    ./admin_tools\
    ./compta
# voir si autres fichiers sont concernés, ie : retouches/settings.py ou retouches/urls.py
