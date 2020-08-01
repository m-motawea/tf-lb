import json
from lib.base import ConfigNotExist
from lib.keepalived import KeepAlivedPeers
from bottle import HTTPResponse, get


@get("/lb-config/cluster/nodes")
def list_nodes():
    try:
        cfg = KeepAlivedPeers.get()
        peers = cfg.list_peers()
    except ConfigNotExist:
        peers = []
    return HTTPResponse(
        json.dumps({"peers": peers}),
        status=200,
        headers={"Content-Type": "application/json"}
    )