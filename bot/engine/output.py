"""Code generation from AST back to Lua."""

from typing import Optional
from bot.engine.ast import (
    ASTNode,
    NodeType,
    Block,
    Assignment,
    LocalAssignment,
    IfStatement,
    WhileStatement,
    ForStatement,
    ForInStatement,
    FunctionDef,
    BinaryOp,
    UnaryOp,
    FunctionCall,
    Index,
    Property,
    TableConstructor,
    FunctionExpression,
    NumberLiteral,
    StringLiteral,
    BooleanLiteral,
    NilLiteral,
    Identifier,
    ReturnStatement,
    BreakStatement,
)


class CodeGenerator:
    """Generate Lua code from AST."""

    def __init__(self, indent: str = "  ", minify: bool = True):
        """Initialize code generator.

        Args:
            indent: Indentation string
            minify: Whether to minify output
        """
        self.indent = indent
        self.minify = minify
        self.indent_level = 0
        self.output = []

    def generate(self, node: ASTNode) -> str:
        """Generate code from AST.

        Args:
            node: Root AST node

        Returns:
            Generated Lua code
        """
        self._generate_node(node)
        code = "".join(self.output)
        if self.minify:
            code = self._minify(code)
        return code

    def _generate_node(self, node: ASTNode) -> None:
        """Generate code for node."""
        if node is None:
            return

        if isinstance(node, Block):
            self._generate_block(node)
        elif isinstance(node, LocalAssignment):
            self._generate_local_assign(node)
        elif isinstance(node, Assignment):
            self._generate_assign(node)
        elif isinstance(node, FunctionDef):
            self._generate_function_def(node)
        elif isinstance(node, IfStatement):
            self._generate_if_stmt(node)
        elif isinstance(node, WhileStatement):
            self._generate_while_stmt(node)
        elif isinstance(node, ForStatement):
            self._generate_for_stmt(node)
        elif isinstance(node, ForInStatement):
            self._generate_for_in_stmt(node)
        elif isinstance(node, ReturnStatement):
            self._generate_return_stmt(node)
        elif isinstance(node, BreakStatement):
            self._generate_break_stmt(node)
        else:
            self._generate_expression(node)

    def _generate_block(self, node: Block) -> None:
        """Generate block."""
        for stmt in node.statements:
            self._generate_node(stmt)
            self._emit("\n")

    def _generate_local_assign(self, node: LocalAssignment) -> None:
        """Generate local assignment."""
        self._emit("local ")
        self._emit(", ".join(node.names))
        if node.values:
            self._emit(" = ")
            self._emit(", ".join(str(self._expr_to_code(v)) for v in node.values))

    def _generate_assign(self, node: Assignment) -> None:
        """Generate assignment."""
        targets = []
        for target in node.targets:
            targets.append(self._expr_to_code(target))
        self._emit(", ".join(targets))
        self._emit(" = ")
        values = []
        for value in node.values:
            values.append(self._expr_to_code(value))
        self._emit(", ".join(values))

    def _generate_function_def(self, node: FunctionDef) -> None:
        """Generate function definition."""
        self._emit("function ")
        self._emit(node.name)
        self._emit("(")
        self._emit(", ".join(node.params))
        if node.vararg:
            if node.params:
                self._emit(", ")
            self._emit("...")
        self._emit(")\n")
        self.indent_level += 1
        self._generate_node(node.body)
        self.indent_level -= 1
        self._emit("end")

    def _generate_if_stmt(self, node: IfStatement) -> None:
        """Generate if statement."""
        self._emit("if ")
        self._emit(self._expr_to_code(node.condition))
        self._emit(" then\n")
        self.indent_level += 1
        self._generate_node(node.then_block)
        self.indent_level -= 1

        for cond, block in node.elseif_parts:
            self._emit("elseif ")
            self._emit(self._expr_to_code(cond))
            self._emit(" then\n")
            self.indent_level += 1
            self._generate_node(block)
            self.indent_level -= 1

        if node.else_block:
            self._emit("else\n")
            self.indent_level += 1
            self._generate_node(node.else_block)
            self.indent_level -= 1

        self._emit("end")

    def _generate_while_stmt(self, node: WhileStatement) -> None:
        """Generate while statement."""
        self._emit("while ")
        self._emit(self._expr_to_code(node.condition))
        self._emit(" do\n")
        self.indent_level += 1
        self._generate_node(node.body)
        self.indent_level -= 1
        self._emit("end")

    def _generate_for_stmt(self, node: ForStatement) -> None:
        """Generate for statement."""
        self._emit(f"for {node.var} = ")
        self._emit(self._expr_to_code(node.start))
        self._emit(", ")
        self._emit(self._expr_to_code(node.end))
        if node.step:
            self._emit(", ")
            self._emit(self._expr_to_code(node.step))
        self._emit(" do\n")
        self.indent_level += 1
        self._generate_node(node.body)
        self.indent_level -= 1
        self._emit("end")

    def _generate_for_in_stmt(self, node: ForInStatement) -> None:
        """Generate for-in statement."""
        self._emit(f"for {', '.join(node.vars)} in ")
        iterables = [self._expr_to_code(it) for it in node.iterables]
        self._emit(", ".join(iterables))
        self._emit(" do\n")
        self.indent_level += 1
        self._generate_node(node.body)
        self.indent_level -= 1
        self._emit("end")

    def _generate_return_stmt(self, node: ReturnStatement) -> None:
        """Generate return statement."""
        self._emit("return")
        if node.values:
            self._emit(" ")
            values = [self._expr_to_code(v) for v in node.values]
            self._emit(", ".join(values))

    def _generate_break_stmt(self, node: BreakStatement) -> None:
        """Generate break statement."""
        self._emit("break")

    def _generate_expression(self, node: ASTNode) -> None:
        """Generate expression."""
        self._emit(self._expr_to_code(node))

    def _expr_to_code(self, node: ASTNode) -> str:
        """Convert expression to code string."""
        if node is None:
            return ""

        if isinstance(node, NumberLiteral):
            return node.value
        elif isinstance(node, StringLiteral):
            return self._escape_string(node.value)
        elif isinstance(node, BooleanLiteral):
            return "true" if node.value else "false"
        elif isinstance(node, NilLiteral):
            return "nil"
        elif isinstance(node, Identifier):
            return node.name
        elif isinstance(node, BinaryOp):
            left = self._expr_to_code(node.left)
            right = self._expr_to_code(node.right)
            return f"({left} {node.op} {right})"
        elif isinstance(node, UnaryOp):
            operand = self._expr_to_code(node.operand)
            return f"({node.op} {operand})"
        elif isinstance(node, FunctionCall):
            func = self._expr_to_code(node.func)
            args = ", ".join(self._expr_to_code(arg) for arg in node.args)
            return f"{func}({args})"
        elif isinstance(node, Index):
            table = self._expr_to_code(node.table)
            index = self._expr_to_code(node.index)
            return f"{table}[{index}]"
        elif isinstance(node, Property):
            obj = self._expr_to_code(node.object)
            return f"{obj}.{node.property}"
        elif isinstance(node, TableConstructor):
            return self._table_to_code(node)
        elif isinstance(node, FunctionExpression):
            return self._function_expr_to_code(node)
        else:
            return str(node)

    def _escape_string(self, s: str) -> str:
        """Escape string for Lua."""
        s = s.replace("\\", "\\\\")
        s = s.replace('"', '\\"')
        s = s.replace("\n", "\\n")
        s = s.replace("\r", "\\r")
        s = s.replace("\t", "\\t")
        return f'"{s}"'

    def _table_to_code(self, node: TableConstructor) -> str:
        """Generate table constructor code."""
        if not node.fields:
            return "{}"
        fields = []
        for key, value in node.fields:
            if key is None:
                fields.append(self._expr_to_code(value))
            elif isinstance(key, Identifier):
                fields.append(f"{key.name} = {self._expr_to_code(value)}")
            else:
                fields.append(f"[{self._expr_to_code(key)}] = {self._expr_to_code(value)}")
        return "{" + ", ".join(fields) + "}"

    def _function_expr_to_code(self, node: FunctionExpression) -> str:
        """Generate function expression code."""
        params = ", ".join(node.params)
        if node.vararg:
            if node.params:
                params += ", "
            params += "..."
        # Simplified - full implementation would need proper code generation
        return f"function({params}) ... end"

    def _emit(self, text: str) -> None:
        """Emit code."""
        if text == "\n":
            self.output.append("\n")
            self.output.append(self.indent * self.indent_level)
        else:
            self.output.append(text)

    def _minify(self, code: str) -> str:
        """Minify code."""
        # Remove comments
        lines = code.split("\n")
        lines = [line.split("--")[0].strip() for line in lines]
        # Remove empty lines
        lines = [line for line in lines if line]
        # Join with minimal whitespace
        return " ".join(lines)
