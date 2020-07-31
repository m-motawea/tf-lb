from lib.keepalived import KeepAlivedPeers
from lib.base import ConfigNotExist
import time
import os
import redis
import jinja2
import netifaces as ni

templateLoader = jinja2.FileSystemLoader(searchpath="/services/lib/templates")
# templateLoader = jinja2.FileSystemLoader(searchpath="/home/maged/Code/tf-loadbalancer/services/lib/templates")
templateEnv = jinja2.Environment(loader=templateLoader)

def update_peers():
    ni.ifaddresses('eth0')
    node_ip = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']
    try:
        cfg = KeepAlivedPeers.get()
    except ConfigNotExist:
        cfg = KeepAlivedPeers()
    peer_ips = cfg.list_peers()
    node_state = os.environ.get("KEEPALIVED_STATE", "MASTER")
    template = templateEnv.get_template("keepalived.conf")
    output = template.render(node_state=node_state, peer_ips=peer_ips, node_ip=node_ip)
    with open("/etc/keepalived/keepalived.conf", "w") as f:
        f.write(output)

def process_loop(self):
    cluster_version = 0
    while True:
        try:
            cl = redis.Redis(
                host=os.environ.get("REDIS_IP_ADDRESS", "127.0.0.1"),
                port=int(os.environ.get("REDIS_PORT", 6379)),
            )
            current_version = cl.get("CLUSTER_VERSION")
            if current_version and int(current_version.decode()) > cluster_version:
                update_peers()
                res = os.system("service keepalived reload")
                if res == 0:
                    cluster_version = int(current_version.decode())
        except Exception as e:
            print(e)
        time.sleep(10)


if __name__ == "__main__":
    update_peers()

    