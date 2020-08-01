import click
import requests
from nacl.signing import SigningKey
from nacl.encoding import HexEncoder
import binascii
import os, json

@click.group()
def cli():
    pass

def sign_message(signing_key, message):
    if isinstance(signing_key, str):
        signing_key = binascii.unhexlify(signing_key)
    if isinstance(signing_key, bytes):
        signing_key = SigningKey(signing_key)
    if isinstance(message, str):
        message = message.encode()
    return signing_key.sign(message, encoder=HexEncoder)


@cli.command()
@click.argument('name')
@click.option(
    '--signing-key',
    help='your signing key in hex',
)
@click.option(
    '--address',
    help='ip address of your lb',
)
def add_upstream(name, signing_key=None, address=None):
    body = {"name": name}
    signing_key = signing_key or os.environ["SIGNING_KEY"]
    signature = sign_message(signing_key, json.dumps(body))
    address = address or "localhost"
    headers = {
        "Signature": signature.decode(),
        "Content-Type": "application/json"
    }
    res = requests.post(f"https://{address}/lb-config/upstreams", json.dumps(body), headers=headers)
    print(res.text)
    return res.status_code == 201


@cli.command()
@click.argument('name')
@click.option(
    '--signing-key',
    help='your signing key in hex',
)
@click.option(
    '--address',
    help='ip address of your lb',
)
def delete_upstream(name, signing_key=None, address=None):
    signing_key = signing_key or os.environ["SIGNING_KEY"]
    signature = sign_message(signing_key, json.dumps({"upstream_name": name}))
    address = address or "localhost"
    headers = {
        "Signature": signature.decode(),
        "Content-Type": "application/json"
    }
    res = requests.delete(f"https://{address}/lb-config/upstreams/{name}", headers=headers)
    if res.status_code == 204:
        print(f"upstream {name} deleted")
    return res.status_code == 204


@cli.command()
@click.option(
    '--address',
    help='ip address of your lb',
)
def list_upstreams(address=None):
    address = address or "localhost"
    headers = {
        "Content-Type": "application/json"
    }
    res = requests.get(f"https://{address}/lb-config/upstreams", headers=headers)
    print(res.text)
    return res.status_code == 200


@cli.command()
@click.argument('name')
@click.option(
    '--address',
    help='ip address of your lb',
)
def list_backends(name, address=None):
    address = address or "localhost"
    headers = {
        "Content-Type": "application/json"
    }
    res = requests.get(f"https://{address}/lb-config/upstreams/{name}", headers=headers)
    print(res.text)
    return res.status_code == 200


@cli.command()
@click.argument('name')
@click.argument('dst_ip')
@click.argument('dst_port')
@click.argument('weight', default=100)
@click.option(
    '--signing-key',
    help='your signing key in hex',
)
@click.option(
    '--address',
    help='ip address of your lb',
)
def add_backend(name, dst_ip, dst_port, weight=100, signing_key=None, address=None):
    body = {"dst_ip": dst_ip, "dst_port": dst_port, "weight": weight}
    signing_key = signing_key or os.environ["SIGNING_KEY"]
    signature = sign_message(signing_key, json.dumps(body))
    address = address or "localhost"
    headers = {
        "Signature": signature.decode(),
        "Content-Type": "application/json"
    }
    res = requests.post(f"https://{address}/lb-config/upstreams/{name}", json.dumps(body), headers=headers)
    print(res.text)
    return res.status_code == 201


@cli.command()
@click.argument('name')
@click.argument('dst_ip')
@click.argument('dst_port')
@click.argument('weight', default=100)
@click.option(
    '--signing-key',
    help='your signing key in hex',
)
@click.option(
    '--address',
    help='ip address of your lb',
)
def delete_backend(name, dst_ip, dst_port, weight=100, signing_key=None, address=None):
    body = {"dst_ip": dst_ip, "dst_port": dst_port, "weight": weight}
    signing_key = signing_key or os.environ["SIGNING_KEY"]
    signature = sign_message(signing_key, json.dumps(body))
    address = address or "localhost"
    headers = {
        "Signature": signature.decode(),
        "Content-Type": "application/json"
    }
    res = requests.post(f"https://{address}/lb-config/upstreams/{name}/delete", json.dumps(body), headers=headers)
    if res.status_code == 204:
        print(f"backend {dst_ip}:{dst_port} weight: {weight} deleted successfully")
    if res.status_code == 404:
        print(f"backend {dst_ip}:{dst_port} weight: {weight} doesn't exist")
    return res.status_code == 204


@cli.command()
@click.argument('name')
@click.argument('upstream')
@click.option(
    '--signing-key',
    help='your signing key in hex',
)
@click.option(
    '--address',
    help='ip address of your lb',
)
def add_server(name, upstream, signing_key=None, address=None):
    body = {"name": name, "upstream": upstream}
    signing_key = signing_key or os.environ["SIGNING_KEY"]
    signature = sign_message(signing_key, json.dumps(body))
    address = address or "localhost"
    headers = {
        "Signature": signature.decode(),
        "Content-Type": "application/json"
    }
    res = requests.post(f"https://{address}/lb-config/servers", json.dumps(body), headers=headers)
    print(res.text)
    return res.status_code == 201


@cli.command()
@click.argument('name')
@click.option(
    '--signing-key',
    help='your signing key in hex',
)
@click.option(
    '--address',
    help='ip address of your lb',
)
def delete_server(name, signing_key=None, address=None):
    signing_key = signing_key or os.environ["SIGNING_KEY"]
    signature = sign_message(signing_key, json.dumps({"server_name": name}))
    address = address or "localhost"
    headers = {
        "Signature": signature.decode(),
        "Content-Type": "application/json"
    }
    res = requests.delete(f"https://{address}/lb-config/servers/{name}", headers=headers)
    if res.status_code == 204:
        print(f"server {name} deleted")
    return res.status_code == 204


@cli.command()
@click.option(
    '--address',
    help='ip address of your lb',
)
def list_peers(address=None):
    address = address or "localhost"
    headers = {
        "Content-Type": "application/json"
    }
    res = requests.get(f"https://{address}/lb-config/cluster/nodes", headers=headers)
    print(res.text)
    return res.status_code == 200

if __name__ == "__main__":
    cli()
