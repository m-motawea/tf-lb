#!/bin/bash
if ["$3" == "MASTER"]; then 
    pkill -9 trc
    /trc -local 127.0.0.1:80 -local-tls 127.0.0.1:443 -remote $TFGATEWAY &