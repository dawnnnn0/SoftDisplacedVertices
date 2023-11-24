#!/bin/sh

awk '
/CRAB project directory:/ {name=substr($4,49) } 
/Publication status/ { status=$9 $10}
/Output dataset:/ {dset=$3}
/Summary of run jobs:/ { print name ": " status " : " dset }
' status.log
