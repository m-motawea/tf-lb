import json
from lib.nginx import Upstream, ResourceInUse
from lib.base import ConfigNotExist
from bottle import post, HTTPResponse, get, delete
from decorators import json_body_validation

# TODO: add delete and update apis
__all__ = ["list_upstreams", "add_upstream", "list_backends", "add_backend"]

@get("/lb-config/upstreams")
def list_upstreams():
    upstreams = Upstream.list_upstreams()
    return HTTPResponse(
        json.dumps({"upstreams": upstreams}),
        status=200,
        headers={"Content-Type": "application/json"}
    )


@post("/lb-config/upstreams")
@json_body_validation
def add_upstream(body):
    """
    body: name
    """
    name = body.get("name")
    if not name:
        return HTTPResponse(
            json.dumps({"error": "missing key `name` in body"}),
            status=400,
            headers={"Content-Type": "application/json"}
        )
    u = Upstream(name)
    u.save()
    return HTTPResponse(
        json.dumps(body),
        status=201,
        headers={"Content-Type": "application/json"}
    )

@delete("/lb-config/upstreams/<upstream_name>")
def delete_upstream(upstream_name):
    try:
        u = Upstream.get(upstream_name)
    except ConfigNotExist:
        return HTTPResponse(
                json.dumps({"error": f"upstream {upstream_name} doesn't exist"}),
                status=404,
                headers={"Content-Type": "application/json"}
            )
    try:
        u.delete()
    except ResourceInUse:
        return HTTPResponse(
                json.dumps({"error": f"upstream {upstream_name} is bound to a server. please delete the server first"}),
                status=400,
                headers={"Content-Type": "application/json"}
            )
    return HTTPResponse(
        json.dumps({"success": True}),
        status=204,
        headers={"Content-Type": "application/json"}
    )


@get("/lb-config/upstreams/<upstream_name>")
def list_backends(upstream_name):
    try:
        u = Upstream.get(upstream_name)
    except ConfigNotExist:
        if upstream_name in Upstream.list_upstreams():
            backends = []
        else:
            return HTTPResponse(
                json.dumps({"error": f"upstream {upstream_name} doesn't exist"}),
                status=404,
                headers={"Content-Type": "application/json"}
            )
    else:
        backends = u.list_servers()
    return HTTPResponse(
        json.dumps({"backends": backends}),
        status=200,
        headers={"Content-Type": "application/json"}
    )

@post("/lb-config/upstreams/<upstream_name>")
@json_body_validation
def add_backend(upstream_name, body):
    """
    body: dst_ip, dst_port, weight
    """
    for key in ["dst_ip", "dst_port"]:
        if key not in body:
            return HTTPResponse(
                json.dumps({"error": f"missing key `{key}` in body"}),
                status=400,
                headers={"Content-Type": "application/json"}
            )
    try:
        u = Upstream.get(upstream_name)
    except ConfigNotExist:
        if upstream_name in Upstream.list_upstreams():
            u = Upstream(upstream_name)
        else:
            return HTTPResponse(
                json.dumps({"error": f"upstream {upstream_name} doesn't exist"}),
                status=404,
                headers={"Content-Type": "application/json"}
            )
    u.add_server(body["dst_ip"], body["dst_port"], body.get("weight", 100))
    u.save()

    return HTTPResponse(
        json.dumps(body),
        status=201,
        headers={"Content-Type": "application/json"}
    )