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

@dataclass
class PiList:
    elements: list['PiExpression']

@dataclass
class PiTuple:
    elements: tuple['PiExpression', ...]

@dataclass
class PiString:
    value: str

@dataclass
class PiFunctionDef:
    name: str
    arg_names: list[str]
    vararg: str | None
    body: list['PiStatement']

@dataclass
class PiFunctionCall:
    function: 'PiExpression'
    args: list['PiExpression']

@dataclass
class PiFor:
    var: str
    iterable: 'PiExpression'
    body: list['PiStatement']

@dataclass
class PiBreak:
    pass

@dataclass
class PiContinue:
    pass

@dataclass
class PiIn:
    element: 'PiExpression'
    container: 'PiExpression'

@dataclass
class PiRaise:
    exception: 'PiExpression'

@dataclass
class PiTryExcept:
    try_body: list['PiStatement']
    except_var: str | None
    except_body: list['PiStatement']

@dataclass
class PiPrimitiveOp:
    name: str
    args: list['PiExpression']

@dataclass
class PiReturn:
    value: 'PiExpression'

PiValue = PiNumber | PiBool | PiNone | PiList | PiTuple | PiString

PiExpression = (
    PiValue
    | PiVariable
    | PiBinaryOperation
    | PiNot
    | PiAnd
    | PiOr
    | PiPrint
    | PiFunctionCall
    | PiIn
    | PiPrimitiveOp
)

PiStatement = (
    PiAssignment
    | PiIfThenElse
    | PiWhile
    | PiFor
    | PiBreak
    | PiContinue
    | PiRaise
    | PiTryExcept
    | PiFunctionDef
    | PiReturn
    | PiExpression
)

PiProgram = list[PiStatement]
