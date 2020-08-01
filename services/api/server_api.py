import json
from lib.nginx import Server
from lib.base import ConfigNotExist
from bottle import post, HTTPResponse, get, delete
from decorators import json_body_validation


@get("/lb-config/servers")
def list_servers():
    servers = Server.list_servers()
    return HTTPResponse(
        json.dumps({"servers": servers}),
        status=200,
        headers={"Content-Type": "application/json"}
    )


@post("/lb-config/servers")
@json_body_validation
def add_server(body):
    """
    body: name
    """
    name = body.get("name")
    upstream = body.get("upstream")
    if not name:
        return HTTPResponse(
            json.dumps({"error": "missing keys in body"}),
            status=400,
            headers={"Content-Type": "application/json"}
        )
    s = Server(name, upstream)
    s.save()
    return HTTPResponse(
        json.dumps(body),
        status=201,
        headers={"Content-Type": "application/json"}
    )

@get("/lb-config/servers/<server_name>")
def get_server(server_name):
    try:
        s = Server.get(server_name)
    except ConfigNotExist:
        return HTTPResponse(
            json.dumps({"error": f"server {server_name} does not exist"}),
            status=404,
            headers={"Content-Type": "application/json"}
        )
    return HTTPResponse(
            json.dumps({"upstream": s.upstream_name}),
            status=200,
            headers={"Content-Type": "application/json"}
        )

@delete("/lb-config/servers/<server_name>")
def delete_server(server_name):
    try:
        s = Server.get(server_name)
    except ConfigNotExist:
        return HTTPResponse(
            json.dumps({"error": f"server {server_name} does not exist"}),
            status=404,
            headers={"Content-Type": "application/json"}
        )
    s.delete()
    return HTTPResponse(
        json.dumps({"success": True}),
        status=204,
        headers={"Content-Type": "application/json"}
    )
