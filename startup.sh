#!/bin/sh

dir=$(pwd) 
cd /home/pi/DeviceShape/

echo "Startup running..."
date >> ./update.log

output=&(/usr/bin/git pull)

echo $output >> ./update.log

cd $dir
