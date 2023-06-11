#!/bin/bash

# export IP_ADDR=$(awk 'END{print $1}' /etc/hosts)

sleep 25
./nr-ue -c /mnt/ueransim/open5gs-ue2.yaml > /mnt/log/ue2.log 2>&1
