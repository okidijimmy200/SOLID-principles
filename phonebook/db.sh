#!/bin/bash
# this declares that current user is a sudoer

sudo service mysql status | grep "stopped\|dead"
if [ $? -eq 0 ]; then
      sudo service mysql start
fi
pytest 