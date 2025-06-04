from typing import Union, List, Tuple, Callable
from dataclasses import dataclass
from pithon.syntax import (
    PiNumber, PiBool, PiNone, PiString, PiFunctionDef,
)
from pithon.evaluator.envframe import EnvFrame

PrimitiveFunction = Callable[..., 'EnvValue']

@dataclass
class FunctionClosure:
    funcdef: PiFunctionDef
    closure_env: EnvFrame

# EnvValue can be a value, a closure, or a primitive function (callable)
EnvValue = Union[
    PiNumber,
    PiBool,
    PiNone,
    PiString,
    List['EnvValue'],
    Tuple['EnvValue', ...],
    FunctionClosure,
    PrimitiveFunction
]
