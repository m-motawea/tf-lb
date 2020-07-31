import jinja2 
from lib.nginx import Upstream, Server
import time
import os
import redis

templateLoader = jinja2.FileSystemLoader(searchpath="/services/lib/templates")
# templateLoader = jinja2.FileSystemLoader(searchpath="/home/maged/Code/tf-loadbalancer/services/lib/templates")
templateEnv = jinja2.Environment(loader=templateLoader)

def update_upstreams():
    all_upstreams = Upstream.list_upstreams()
    render_upstreams = []
    for upstream in all_upstreams:
        u = Upstream.get(upstream)
        u.name = upstream
        u.servers = u.list_servers()
        render_upstreams.append(u)
    template = templateEnv.get_template("upstreams.conf")
    output = template.render(upstreams=render_upstreams)
    with open("/etc/nginx/upstreams.conf", "w") as f:
        f.write(output)

def update_servers():
    all_servers = Server.list_servers()
    render_servers = []
    for server in all_servers:
        s = Server.get(server)
        render_servers.append(s)
    template = templateEnv.get_template("servers.conf")
    output = template.render(servers=render_servers)
    with open("/etc/nginx/servers.conf", "w") as f:
        f.write(output)

def daemon_loop():
    config_version = 0
    while True:
        try:
            cl = redis.Redis(
                host=os.environ.get("REDIS_IP_ADDRESS", "127.0.0.1"),
                port=int(os.environ.get("REDIS_PORT", 6379)),
            )
            current_version = cl.get("CONFIG_VERSION")
            if current_version and int(current_version.decode()) > config_version:
                update_upstreams()
                update_servers()
                res = os.system("service nginx reload")
                if res == 0:
                    config_version = int(current_version.decode())
        except Exception as e:
            print(e)
        time.sleep(10)



if __name__ == "__main__":
    daemon_loop()
