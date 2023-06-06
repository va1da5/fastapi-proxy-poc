# FastAPI Reverse Proxy Proof-of-Concept

The repository contains code that implements functionality to proxy and intercept requests sent to the [Vault HTTP API](https://developer.hashicorp.com/vault/api-docs/system).

## Usage

```bash
# create virtual environment
python3 -m venv .venv
source .venv/bin/active

# install dependencies
pip install -U pip
pip install -r requirements.txt

# start Vault development container
docker-compose up -d

# start proxy development server
uvicorn proxy:app --reload
```

## References

- [Can fastapi proxy another site as a response to the request?](https://github.com/tiangolo/fastapi/issues/1788)
