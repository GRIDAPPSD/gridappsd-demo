#!/bin/bash

IPADDRESS="54.184.236.31"

sed -r '/^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}[[:space:]]gridappsd/d' /etc/hosts > /tmp/hosts
echo "${IPADDRESS} gridappsd" >> /tmp/hosts
cat /tmp/hosts | sudo tee /etc/hosts