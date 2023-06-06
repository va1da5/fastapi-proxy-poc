.PHONY: dev
dev:
	uvicorn proxy:app --reload
