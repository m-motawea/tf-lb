from bottle import request, HTTPResponse
from functools import wraps
import json


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