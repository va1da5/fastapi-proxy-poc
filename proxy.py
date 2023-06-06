import json
import os
from collections import UserDict
from typing import Any, Mapping

import httpx
from fastapi import FastAPI
from httpx import Response as HttpxResponse
from starlette.requests import Request
from starlette.responses import Response

from store import Store

VAULT_ADDR = os.environ["VAULT_ADDR"]

app = FastAPI()
client = httpx.AsyncClient(base_url=VAULT_ADDR)
store = Store(path="./store.json")


def patch_response(response: HttpxResponse) -> Mapping[Any, Any]:
    response_data = response.json()

    if "otp" in response_data:
        store["otp"] = response_data["otp"]
        del response_data["otp"]

    if "encoded_root_token" in response_data:
        store["encoded_root_token"] = response_data["encoded_root_token"]
        del response_data["encoded_root_token"]
        del response_data["encoded_token"]

    if "keys_base64" in response_data:
        store["keys_base64"] = response_data["keys_base64"]
        del response_data["keys_base64"]
        del response_data["keys"]

    return response_data


async def _reverse_proxy(request: Request):
    url = httpx.URL(path=request.url.path, query=request.url.query.encode("utf-8"))
    rp_req = client.build_request(request.method, url, headers=request.headers.raw, content=await request.body())
    rp_resp = await client.send(rp_req, stream=False)

    try:
        response_data = patch_response(rp_resp)
        rp_content = json.dumps(response_data).encode("utf-8")
    except Exception as exc:
        print(exc)
        rp_content = rp_resp.content

    return Response(
        rp_content,
        status_code=rp_resp.status_code,
        headers={**rp_resp.headers, **{"content-length": str(len(rp_content))}},
    )


app.add_route("/v1/{path:path}", _reverse_proxy, ["GET", "POST", "PUT", "DELETE"])


@app.get("/")
def index():
    return {"Hello": "Proxy"}
