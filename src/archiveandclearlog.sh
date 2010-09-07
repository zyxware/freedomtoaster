#!/bin/bash

export LOGFILENAME=log.txt

if [ ! -e $LOGFILENAME ]
then
  echo 'No log to archive'
  exit
fi

cp $LOGFILENAME logarchive/`date +%Y-%m-%d-%H-%M-%S`.log
cat $LOGFILENAME >> logarchive/cumulative.log
rm $LOGFILENAME
