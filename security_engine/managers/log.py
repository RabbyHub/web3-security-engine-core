from functools import wraps
from types import FunctionType
from typing import Callable, Any, Tuple

from security_engine.runtime.context import BaseContext


class LogManager(object):
    
    def __init__(self, handlers=[]) -> None:
        self.handlers = handlers

    def load(self):
        pass

    def add_handler(self, handler):
        self.handlers.append(handler)

    def output(self, context):
        for handler in self.handlers:
            handler.output(context)

    def execute(self, fn: FunctionType, *args: Tuple[Any], **kwargs: Any) -> Any:
        res = fn(*args, **kwargs)
        if args and isinstance(args[1], BaseContext):
            self.output(args[1])
        return res

    def __call__(self, fn: FunctionType) -> Callable[..., Any]:

        @wraps(fn)
        def wrapper(*args: Tuple[Any], **kwargs: Any) -> Any:
            return self.execute(fn, *args, **kwargs)

        return wrapper
