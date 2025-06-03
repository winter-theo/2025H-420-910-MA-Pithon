from typing import Union, List, Tuple, Callable
from pithon.syntax import (
    PiNumber, PiBool, PiNone, PiString, PiFunctionDef,
)

class FunctionClosure:
    def __init__(self, funcdef: PiFunctionDef, closure_env: list[tuple[str, 'EnvValue']]):
        self.funcdef = funcdef
        self.closure_env = closure_env.copy()

# EnvValue can be a value, a closure, or a primitive function (callable)
EnvValue = Union[
    PiNumber,
    PiBool,
    PiNone,
    PiString,
    List['EnvValue'],
    Tuple['EnvValue', ...],
    FunctionClosure,
    Callable[..., 'EnvValue']  # primitive functions
]
