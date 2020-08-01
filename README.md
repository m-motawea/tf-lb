# tf-lb
this is a prof-of-concept load balancer cluster solution for the tfgrid (wip). it has a few APIs to update nginx config and list cluster nodes.
it includes a trc binary and runs on the active nodes to expose the cluster through tfgateways.

### Environment Vars:
check env.sh

### Configure Servers and Upstreams:
check example.sh

### Dependencies:
this solution depends on redis to store nginx and keepalived config and discover cluster nodes.
