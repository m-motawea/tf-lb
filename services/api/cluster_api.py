import json
from lib.keepalived import KeepAlivedPeers
from bottle import post, HTTPResponse, get, delete
from api.decorators import json_body_validation


@get("/lb-config/cluster/nodes")
def list_nodes():
    cfg = KeepAlivedPeers.get()
    return HTTPResponse(
        json.dumps({"peers": cfg.list_peers()}),
        status=200,
        headers={"Content-Type": "application/json"}
    )