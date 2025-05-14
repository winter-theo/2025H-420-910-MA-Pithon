from dataclasses import dataclass

@dataclass
class PiNone:
    value: None

@dataclass
class PiNumber:
    value: float

@dataclass
class PiBool:
    value: bool

@dataclass
class PiVariable:
    name: str

@dataclass
class PiBinaryOperation:
    left: 'PiExpression'
    operator: str
    right: 'PiExpression'

@dataclass
class PiAssignment:
    name: str
    value: 'PiExpression'

@dataclass
class PiIfThenElse:
    condition: 'PiExpression'
    then_branch: list['PiStatement']
    else_branch: list['PiStatement']

@dataclass
class PiNot:
    operand: 'PiExpression'

@dataclass
class PiAnd:
    left: 'PiExpression'
    right: 'PiExpression'

@dataclass
class PiOr:
    left: 'PiExpression'
    right: 'PiExpression'

@dataclass
class PiWhile:
    condition: 'PiExpression'
    body: list['PiStatement']

@dataclass
class PiPrint:
    value: 'PiExpression'

PiValue = PiNumber | PiBool | PiNone

PiExpression = (
    PiValue
    | PiVariable
    | PiBinaryOperation
    | PiNot
    | PiAnd
    | PiOr
    | PiPrint
)

PiStatement = (
    PiAssignment
    | PiIfThenElse
    | PiWhile
    | PiExpression
)

PiProgram = list[PiStatement]
