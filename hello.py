"""Hello World worker. The page asks the host to call hello."""

from ox1audio import serve
from ox1audio.cloud.api.default import health


def hello(call):
    name = "world"
    body = call.body
    if isinstance(body, dict):
        given = body.get("name")
        if isinstance(given, str) and given.strip():
            name = given.strip()
    cloud = health.sync(client=call.client)
    call.emit("greeted", {"name": name})
    return {"message": f"Hello, {name}", "cloud": getattr(cloud, "status", None)}


if __name__ == "__main__":
    serve({"hello": hello})
