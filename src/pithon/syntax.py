from dataclasses import dataclass

@dataclass
class PiLiteral:
    value: int

@dataclass
class PiVariable:
    name: str

@dataclass
class PiBinaryOperation:
    left: 'Expression'
    operator: str
    right: 'Expression'

@dataclass
class PiAssignment:
    name: str
    value: 'Expression'

Expression = PiLiteral | PiVariable | PiBinaryOperation

PiSyntaxTree = PiAssignment | Expression
