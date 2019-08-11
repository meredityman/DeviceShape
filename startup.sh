#!/bin/sh

path="/home/pi/DeviceShape/"

check_ipaddr ()
{
  # Here we look for an IP(v4|v6) address when doing ip addr
  # Note we're filtering out 127.0.0.1 and ::1/128 which are the "localhost" ip addresses
  # I'm also removing fe80: which is the "link local" prefix

  ip addr | \
  grep -v 127.0.0.1 | \
  grep -v '::1/128' | \
  grep -v 'inet6 fe80:' | \
  grep -E "inet [[:digit:]]+\.[[:digit:]]+\.[[:digit:]]+\.[[:digit:]]+|inet6" | \
  wc -l
}

check_google ()
{
  netcat -z -w 5 8.8.8.8 53 && echo 1 || echo 0
}



update_repository ()
{
  git pull
}


dir=$(pwd) 
cd "$path"

echo "Waiting for network..."
until [ $(check_google) -eq 1 ]; do
  sleep 2
done

echo "Connected"

echo "---------------------------" >> ./update.log
echo "$(date)\n" >> ./update.log

output=$(update_repository 2>&1)
echo $output >> ./update.log


python3 data_collection.py > run.log

echo "Finished"
cd $dir
