from bottle import request, HTTPResponse
from functools import wraps
import json
from api.utils import verify_signature

def json_body_validation(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        try:
            body = json.loads(request.body.read())
        except Exception as e:
            msg = f"invalid reuqest body {str(e)}"
            return lambda *args, **kwargs : HTTPResponse(
                json.dumps({"error": msg}),
                status=400,
                headers={"Content-Type": "application/json"}
            )
        return func(*args, **kwargs, body=body)
    return decorator

def verify_body_signature(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        if kwargs.get("body"):
            signature = request.headers.get("Signature")
            if not signature:
                return lambda *args, **kwargs : HTTPResponse(
                    json.dumps({"error": "Signature header is missing"}),
                    status=400,
                    headers={"Content-Type": "application/json"}
                )
            res = verify_signature(signature, json.dumps(kwargs["body"]))
            if not res:
                return lambda *args, **kwargs : HTTPResponse(
                    json.dumps({"error": "invalid signature"}),
                    status=401,
                    headers={"Content-Type": "application/json"}
                )
        return func(*args, **kwargs)
    return decorator

def verify_resource_signature(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        signature = request.headers.get("Signature")
        if not signature:
            return lambda *args, **kwargs : HTTPResponse(
                json.dumps({"error": "Signature header is missing"}),
                status=400,
                headers={"Content-Type": "application/json"}
            )
        res = verify_signature(signature, json.dumps(kwargs))
        if not res:
            return lambda *args, **kwargs : HTTPResponse(
                json.dumps({"error": "invalid signature"}),
                status=401,
                headers={"Content-Type": "application/json"}
            )
        return func(*args, **kwargs)
    return decorator
