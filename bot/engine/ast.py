"""Abstract Syntax Tree (AST) nodes for Lua."""

from typing import List, Optional, Any, Dict
from dataclasses import dataclass, field
from enum import Enum


class NodeType(str, Enum):
    """AST node types."""

    # Statements
    BLOCK = "block"
    ASSIGN = "assign"
    LOCAL_ASSIGN = "local_assign"
    IF_STMT = "if_stmt"
    WHILE_STMT = "while_stmt"
    FOR_STMT = "for_stmt"
    FOR_IN_STMT = "for_in_stmt"
    RETURN_STMT = "return_stmt"
    BREAK_STMT = "break_stmt"
    FUNCTION_DEF = "function_def"
    REPEAT_STMT = "repeat_stmt"

    # Expressions
    BINARY_OP = "binary_op"
    UNARY_OP = "unary_op"
    FUNCTION_CALL = "function_call"
    INDEX = "index"
    PROPERTY = "property"
    TABLE_CONS = "table_cons"
    FUNCTION_EXPR = "function_expr"

    # Literals
    NUMBER = "number"
    STRING = "string"
    BOOLEAN = "boolean"
    NIL = "nil"
    IDENTIFIER = "identifier"
    VARARG = "vararg"


@dataclass
class ASTNode:
    """Base AST node."""

    type: NodeType
    line: int = 0
    column: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Block(ASTNode):
    """Block of statements."""

    statements: List[ASTNode] = field(default_factory=list)

    def __post_init__(self):
        self.type = NodeType.BLOCK


@dataclass
class Assignment(ASTNode):
    """Assignment statement."""

    targets: List[ASTNode] = field(default_factory=list)
    values: List[ASTNode] = field(default_factory=list)

    def __post_init__(self):
        self.type = NodeType.ASSIGN


@dataclass
class LocalAssignment(ASTNode):
    """Local variable assignment."""

    names: List[str] = field(default_factory=list)
    values: List[ASTNode] = field(default_factory=list)

    def __post_init__(self):
        self.type = NodeType.LOCAL_ASSIGN


@dataclass
class IfStatement(ASTNode):
    """If statement."""

    condition: ASTNode = None
    then_block: ASTNode = None
    elseif_parts: List[tuple] = field(default_factory=list)  # [(condition, block), ...]
    else_block: Optional[ASTNode] = None

    def __post_init__(self):
        self.type = NodeType.IF_STMT


@dataclass
class WhileStatement(ASTNode):
    """While loop."""

    condition: ASTNode = None
    body: ASTNode = None

    def __post_init__(self):
        self.type = NodeType.WHILE_STMT


@dataclass
class ForStatement(ASTNode):
    """For loop."""

    var: str = ""
    start: ASTNode = None
    end: ASTNode = None
    step: Optional[ASTNode] = None
    body: ASTNode = None

    def __post_init__(self):
        self.type = NodeType.FOR_STMT


@dataclass
class ForInStatement(ASTNode):
    """For-in loop."""

    vars: List[str] = field(default_factory=list)
    iterables: List[ASTNode] = field(default_factory=list)
    body: ASTNode = None

    def __post_init__(self):
        self.type = NodeType.FOR_IN_STMT


@dataclass
class FunctionDef(ASTNode):
    """Function definition."""

    name: str = ""
    params: List[str] = field(default_factory=list)
    vararg: bool = False
    body: ASTNode = None

    def __post_init__(self):
        self.type = NodeType.FUNCTION_DEF


@dataclass
class BinaryOp(ASTNode):
    """Binary operation."""

    op: str = ""
    left: ASTNode = None
    right: ASTNode = None

    def __post_init__(self):
        self.type = NodeType.BINARY_OP


@dataclass
class UnaryOp(ASTNode):
    """Unary operation."""

    op: str = ""
    operand: ASTNode = None

    def __post_init__(self):
        self.type = NodeType.UNARY_OP


@dataclass
class FunctionCall(ASTNode):
    """Function call."""

    func: ASTNode = None
    args: List[ASTNode] = field(default_factory=list)

    def __post_init__(self):
        self.type = NodeType.FUNCTION_CALL


@dataclass
class Index(ASTNode):
    """Table index."""

    table: ASTNode = None
    index: ASTNode = None

    def __post_init__(self):
        self.type = NodeType.INDEX


@dataclass
class Property(ASTNode):
    """Property access."""

    object: ASTNode = None
    property: str = ""

    def __post_init__(self):
        self.type = NodeType.PROPERTY


@dataclass
class TableConstructor(ASTNode):
    """Table constructor."""

    fields: List[tuple] = field(default_factory=list)  # [(key, value), ...] or [value, ...]

    def __post_init__(self):
        self.type = NodeType.TABLE_CONS


@dataclass
class FunctionExpression(ASTNode):
    """Function expression."""

    params: List[str] = field(default_factory=list)
    vararg: bool = False
    body: ASTNode = None

    def __post_init__(self):
        self.type = NodeType.FUNCTION_EXPR


@dataclass
class NumberLiteral(ASTNode):
    """Number literal."""

    value: str = ""

    def __post_init__(self):
        self.type = NodeType.NUMBER


@dataclass
class StringLiteral(ASTNode):
    """String literal."""

    value: str = ""

    def __post_init__(self):
        self.type = NodeType.STRING


@dataclass
class BooleanLiteral(ASTNode):
    """Boolean literal."""

    value: bool = False

    def __post_init__(self):
        self.type = NodeType.BOOLEAN


@dataclass
class NilLiteral(ASTNode):
    """Nil literal."""

    def __post_init__(self):
        self.type = NodeType.NIL


@dataclass
class Identifier(ASTNode):
    """Identifier."""

    name: str = ""

    def __post_init__(self):
        self.type = NodeType.IDENTIFIER


@dataclass
class ReturnStatement(ASTNode):
    """Return statement."""

    values: List[ASTNode] = field(default_factory=list)

    def __post_init__(self):
        self.type = NodeType.RETURN_STMT


@dataclass
class BreakStatement(ASTNode):
    """Break statement."""

    def __post_init__(self):
        self.type = NodeType.BREAK_STMT
