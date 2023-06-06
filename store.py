import json
from collections import UserDict
from typing import Any


class Store(UserDict):
    def __init__(self, *args, path: str = "store.json", **kwargs):
        self.path = path
        self._load()
        super().__init__(self, *args, **kwargs)

    def _store(self):
        with open(self.path, "w", encoding="utf-8") as store_file:
            json.dump(self.data, store_file)

    def _load(self):
        try:
            with open(self.path, "r", encoding="utf-8") as store_file:
                self.data = json.load(store_file)
        except FileNotFoundError:
            self.data = dict()

    def __setitem__(self, key: Any, item: Any) -> None:
        super().__setitem__(key, item)
        self._store()
