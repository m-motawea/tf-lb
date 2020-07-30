import jinja2 
from lib.nginx import Upstream, Server
import time
import os
import daemon

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
    while True:
        update_upstreams()
        update_servers()
        os.system("service nginx reload")
        time.sleep(100)



if __name__ == "__main__":
    with daemon.DaemonContext():
        daemon_loop()
