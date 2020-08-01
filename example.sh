curl -i -k -X POST -d '{"name": "hamada"}' https://172.17.0.2/lb-config/upstreams 

curl -i -k -X POST -d '{"dst_ip": "172.17.0.1", "dst_port": 8000, "weight": 100}' https://172.17.0.2/lb-config/upstreams/hamada 

curl -i -k -X POST -d '{"name": "maglab.com", "upstream": "hamada"}' https://172.17.0.2/lb-config/servers

