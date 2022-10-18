#!/bin/bash
# this declares that current user is a sudoer

TEMP_LOG_FILE=tmp.log
> "$TEMP_LOG_FILE"
nohup sudo ./minio server /minio &> "$TEMP_LOG_FILE" & tail -f "$TEMP_LOG_FILE" & time bash -c 'ulimit -t 5; while true; do true; done'

pytest 