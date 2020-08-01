# tf-lb
this is a proof-of-concept load balancer cluster solution for the tfgrid (wip). it has a few APIs to update nginx config and list cluster nodes.

it includes a trc binary and runs on the active nodes to expose the cluster through tfgateways.

### Environment Vars:
check env.sh

### Configure Servers and Upstreams:
check example.sh

### Dependencies:
this solution depends on redis to store nginx and keepalived config and discover cluster nodes.

### Maain Processes:
1- Nginx

2- Keepalived

3- /services/app.py: provides apis to configure nginx.

4- /services/lbd.py: listens for nginx config changes on redis and updates nginx config.

5- /services/clusterd.py: listens for keepalived peers changes on redis and updates keepalived config.

5- trc: started and stopped by keepalived failover script /failover.sh.
