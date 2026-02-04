import time
import threading
from collections import OrderedDict
from typing import Any, Optional, Callable


class TTLCache:
    def __init__(self, maxsize: int = 512, ttl: int = 900):
        self.maxsize = maxsize
        self.ttl = ttl
        self._data: OrderedDict[str, tuple[float, Any]] = OrderedDict()
        self._lock = threading.Lock()

    def _purge(self) -> None:
        now = time.time()
        keys_to_delete = []
        for k, (exp, _) in self._data.items():
            if exp < now:
                keys_to_delete.append(k)
        for k in keys_to_delete:
            self._data.pop(k, None)
        while len(self._data) > self.maxsize:
            self._data.popitem(last=False)

    def get(self, key: str) -> Optional[Any]:
        with self._lock:
            self._purge()
            if key not in self._data:
                return None
            exp, value = self._data.pop(key)
            if exp < time.time():
                return None
            self._data[key] = (exp, value)
            return value

    def set(self, key: str, value: Any) -> None:
        with self._lock:
            self._purge()
            exp = time.time() + self.ttl
            if key in self._data:
                self._data.pop(key)
            self._data[key] = (exp, value)

    def cached(self, key_builder: Callable[..., str]):
        def decorator(func: Callable[..., Any]):
            async def wrapper(*args, **kwargs):
                key = key_builder(*args, **kwargs)
                cached_value = self.get(key)
                if cached_value is not None:
                    return cached_value
                result = await func(*args, **kwargs)
                if result is not None:
                    self.set(key, result)
                return result

            return wrapper

        return decorator
