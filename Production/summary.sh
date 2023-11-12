#!/bin/sh

awk '/CRAB project directory:/ {name=substr($4,47) } /Publication status/ { print name ": " $9 $10}' status.log
