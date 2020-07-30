curl -X POST -d '{"name": "hamada"}' http://172.17.0.2/lb-config/upstreams 

curl -X POST -d '{"dst_ip": "172.17.0.1", "dst_port": 8000, "weight": 100}' http://172.17.0.2/lb-config/upstreams/hamada 

curl -X POST -d '{"name": "maglab.com", "upstream": "hamada"}' http://172.17.0.2/lb-config/servers

