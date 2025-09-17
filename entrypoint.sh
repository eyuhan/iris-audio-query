#!/bin/sh

# start iris
/iris-main "$@" &

# wait for iris to be ready
/usr/irissys/dev/Cloud/ICM/waitISC.sh

#init iop
iop --init

# load production
iop -m /irisdev/app/community/settings.py

# start production
iop --start Python.Production
