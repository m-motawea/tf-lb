# tf-lb
this is a proof-of-concept load balancer cluster solution for the tfgrid (wip). it has a few APIs to update nginx config and list cluster nodes.

it includes a trc binary and runs on the active nodes to expose the cluster through tfgateways.

### Environment Vars:
check env.sh

### Configure Servers and Upstreams:
The offered APIs require a certain signature scheme to authenticate the requests based on the hex verify key specifed in environment. the signature has been implemented in the client provided.

```
[maged@localhost services]$ python client.py --help
Usage: client.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  add-backend      add backend to the specified upstream
  add-server       create a new nginx server construct
  add-upstream     create a new upstream
  delete-backend   delete the specified backend from upstream
  delete-server    delete the specified nginx server
  delete-upstream  delete upstream
  list-backends    list backends of the specified upstream
  list-peers       list keepalived configured peers
  list-upstreams   list all upstreams
```

### Dependencies:
this solution depends on redis to store nginx and keepalived config and discover cluster nodes.

### Main Processes:
1- Nginx

2- Keepalived

3- /services/app.py: provides apis to configure nginx.

4- /services/lbd.py: listens for nginx config changes on redis and updates nginx config.

5- /services/clusterd.py: listens for keepalived peers changes on redis and updates keepalived config.

6- trc: started and stopped by keepalived failover script /failover.sh.


### TODO:

1- Provide facilities for configuring ssl certificates

2- add relative backend weights for each cluster node
