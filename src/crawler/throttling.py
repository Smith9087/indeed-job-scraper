import threading
import time
from typing import Callable, TypeVar, Optional

T = TypeVar("T")

class RateLimiter:
    """
    Simple thread-safe rate limiter using a token bucket approach.
    """
    def __init__(self, max_calls: int, per_seconds: float):
        self.max_calls = max_calls
        self.per_seconds = per_seconds
        self._lock = threading.Lock()
        self._tokens = max_calls
        self._last = time.monotonic()

    def acquire(self) -> None:
        with self._lock:
            now = time.monotonic()
            elapsed = now - self._last
            # Refill
            refill = (elapsed / self.per_seconds) * self.max_calls
            if refill > 0:
                self._tokens = min(self.max_calls, self._tokens + refill)
                self._last = now

            if self._tokens >= 1:
                self._tokens -= 1
                return
            # Need to wait
            needed = 1 - self._tokens
            seconds = (needed / self.max_calls) * self.per_seconds
            time.sleep(max(seconds, 0.01))
            # After sleep, consume token
            self._tokens = max(self._tokens - 1, 0)

def backoff(func: Callable[[], T], tries: int = 3, first_delay: float = 1.0, factor: float = 2.0,
           max_delay: float = 8.0) -> Optional[T]:
    """
    Retry a callable with exponential backoff.
    """
    delay = first_delay
    last_exc = None
    for attempt in range(tries):
        try:
            return func()
        except Exception as e:
            last_exc = e
            time.sleep(min(delay, max_delay))
            delay *= factor
    if last_exc:
        # Surface the exception as None; caller can handle missing value.
        return None
    return None