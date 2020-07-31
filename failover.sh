#!/bin/bash
if ["$3" == "MASTER"]; then 
    if pgrep -x "trc" > /dev/null; then
        echo "trc is running"
    else
        /trc -local 127.0.0.1:80 -local-tls 127.0.0.1:443 -remote $TFGATEWAY &
    fi
else 
    pkill -9 trc
fi