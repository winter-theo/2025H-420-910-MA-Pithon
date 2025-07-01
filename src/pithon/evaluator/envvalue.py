from typing import Union,  Callable
from dataclasses import dataclass
from pithon.syntax import ( PiFunctionDef,
)
from pithon.evaluator.envframe import EnvFrame

PrimitiveFunction = Callable[..., 'EnvValue']

@dataclass
class FunctionClosure:
    funcdef: PiFunctionDef
    closure_env: EnvFrame

    def __str__(self) -> str:
        return f"<function {self.funcdef.name} at {id(self)}>"

@dataclass
class VList:
    value: list['EnvValue']

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return repr(self.value)

@dataclass
class VTuple:
    value: tuple['EnvValue', ...]

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return repr(self.value)

@dataclass
class VNumber:
    value: float

    def __str__(self) -> str:
        return str(self.value)


    def __repr__(self) -> str:
        return repr(self.value)

@dataclass
class VBool:
    value: bool

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return repr(self.value)

@dataclass
class VNone:
    value: None = None

    def __str__(self) -> str:
        return str(None)

    def __repr__(self) -> str:
        return repr(self.value)

@dataclass
class VString:
    value: str

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return repr(self.value)

EnvValue = Union[
    VNumber,
    VBool,
    VNone,
    VString,
    VList,
    VTuple,
    FunctionClosure,
    PrimitiveFunction
]
