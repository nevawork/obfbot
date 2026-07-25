"""Parser for Lua code to AST."""

from typing import List, Optional
from bot.engine.tokenizer import Token, TokenType, Tokenizer
from bot.engine.ast import (
    ASTNode,
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
from bot.logger import logger


class Parser:
    """Parses Lua tokens to AST."""

    def __init__(self, tokens: List[Token]):
        """Initialize parser.

        Args:
            tokens: List of tokens from tokenizer
        """
        self.tokens = tokens
        self.pos = 0

    @classmethod
    def from_code(cls, code: str) -> "Parser":
        """Create parser from code.

        Args:
            code: Lua code

        Returns:
            Parser instance
        """
        tokenizer = Tokenizer(code)
        tokens = tokenizer.tokenize()
        return cls(tokens)

    def parse(self) -> Block:
        """Parse tokens to AST.

        Returns:
            Root block node
        """
        return self._parse_block()

    def _current(self) -> Optional[Token]:
        """Get current token."""
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def _peek(self, offset: int = 1) -> Optional[Token]:
        """Peek ahead."""
        pos = self.pos + offset
        return self.tokens[pos] if pos < len(self.tokens) else None

    def _advance(self) -> Token:
        """Consume current token."""
        token = self._current()
        self.pos += 1
        return token

    def _match(self, *types: TokenType) -> bool:
        """Check if current token matches any type."""
        token = self._current()
        return token and token.type in types

    def _consume(self, expected: TokenType, message: str = "") -> Token:
        """Consume token of expected type."""
        if not self._match(expected):
            token = self._current()
            raise SyntaxError(f"{message} at {token}")
        return self._advance()

    def _skip_comments(self) -> None:
        """Skip comment tokens."""
        while self._match(TokenType.COMMENT):
            self._advance()

    def _parse_block(self) -> Block:
        """Parse block of statements."""
        block = Block()
        self._skip_comments()

        while not self._match(TokenType.EOF) and not self._is_block_end():
            self._skip_comments()
            if self._is_block_end():
                break
            stmt = self._parse_statement()
            if stmt:
                block.statements.append(stmt)
            self._skip_comments()

        return block

    def _is_block_end(self) -> bool:
        """Check if we're at block end."""
        return self._match(
            TokenType.EOF,
            TokenType.KEYWORD,
        ) and self._current() and self._current().value in (
            "end",
            "else",
            "elseif",
            "until",
        )

    def _parse_statement(self) -> Optional[ASTNode]:
        """Parse a statement."""
        token = self._current()

        if not token:
            return None

        # Keywords
        if token.type == TokenType.KEYWORD:
            if token.value == "local":
                return self._parse_local_assign()
            elif token.value == "function":
                return self._parse_function_def()
            elif token.value == "if":
                return self._parse_if_stmt()
            elif token.value == "while":
                return self._parse_while_stmt()
            elif token.value == "for":
                return self._parse_for_stmt()
            elif token.value == "repeat":
                return self._parse_repeat_stmt()
            elif token.value == "return":
                return self._parse_return_stmt()
            elif token.value == "break":
                self._advance()
                return BreakStatement()

        # Assignment or expression statement
        return self._parse_assignment_or_call()

    def _parse_local_assign(self) -> LocalAssignment:
        """Parse local assignment."""
        self._consume(TokenType.KEYWORD, "Expected 'local'")
        names = [self._consume(TokenType.IDENTIFIER).value]

        while self._match(TokenType.COMMA):
            self._advance()
            names.append(self._consume(TokenType.IDENTIFIER).value)

        values = []
        if self._match(TokenType.ASSIGN):
            self._advance()
            values.append(self._parse_expression())
            while self._match(TokenType.COMMA):
                self._advance()
                values.append(self._parse_expression())

        return LocalAssignment(names=names, values=values)

    def _parse_function_def(self) -> FunctionDef:
        """Parse function definition."""
        self._consume(TokenType.KEYWORD, "Expected 'function'")
        name = self._consume(TokenType.IDENTIFIER).value

        self._consume(TokenType.LPAREN)
        params, vararg = self._parse_params()
        self._consume(TokenType.RPAREN)

        body = self._parse_block()
        self._consume(TokenType.KEYWORD, "Expected 'end'")

        return FunctionDef(name=name, params=params, vararg=vararg, body=body)

    def _parse_params(self) -> tuple:
        """Parse function parameters."""
        params = []
        vararg = False

        if self._match(TokenType.IDENTIFIER):
            params.append(self._advance().value)
            while self._match(TokenType.COMMA):
                self._advance()
                if self._match(TokenType.KEYWORD) and self._current().value == "...":
                    vararg = True
                    self._advance()
                    break
                params.append(self._consume(TokenType.IDENTIFIER).value)

        return params, vararg

    def _parse_if_stmt(self) -> IfStatement:
        """Parse if statement."""
        self._consume(TokenType.KEYWORD, "Expected 'if'")
        condition = self._parse_expression()
        self._consume(TokenType.KEYWORD, "Expected 'then'")
        then_block = self._parse_block()

        elseif_parts = []
        while self._match(TokenType.KEYWORD) and self._current().value == "elseif":
            self._advance()
            elseif_cond = self._parse_expression()
            self._consume(TokenType.KEYWORD, "Expected 'then'")
            elseif_block = self._parse_block()
            elseif_parts.append((elseif_cond, elseif_block))

        else_block = None
        if self._match(TokenType.KEYWORD) and self._current().value == "else":
            self._advance()
            else_block = self._parse_block()

        self._consume(TokenType.KEYWORD, "Expected 'end'")

        return IfStatement(
            condition=condition,
            then_block=then_block,
            elseif_parts=elseif_parts,
            else_block=else_block,
        )

    def _parse_while_stmt(self) -> WhileStatement:
        """Parse while statement."""
        self._consume(TokenType.KEYWORD, "Expected 'while'")
        condition = self._parse_expression()
        self._consume(TokenType.KEYWORD, "Expected 'do'")
        body = self._parse_block()
        self._consume(TokenType.KEYWORD, "Expected 'end'")

        return WhileStatement(condition=condition, body=body)

    def _parse_for_stmt(self) -> ASTNode:
        """Parse for or for-in statement."""
        self._consume(TokenType.KEYWORD, "Expected 'for'")
        var = self._consume(TokenType.IDENTIFIER).value

        if self._match(TokenType.ASSIGN):
            # Numeric for
            self._advance()
            start = self._parse_expression()
            self._consume(TokenType.COMMA)
            end = self._parse_expression()
            step = None
            if self._match(TokenType.COMMA):
                self._advance()
                step = self._parse_expression()
            self._consume(TokenType.KEYWORD, "Expected 'do'")
            body = self._parse_block()
            self._consume(TokenType.KEYWORD, "Expected 'end'")
            return ForStatement(var=var, start=start, end=end, step=step, body=body)
        else:
            # For-in
            vars = [var]
            while self._match(TokenType.COMMA):
                self._advance()
                vars.append(self._consume(TokenType.IDENTIFIER).value)
            self._consume(TokenType.KEYWORD, "Expected 'in'")
            iterables = [self._parse_expression()]
            while self._match(TokenType.COMMA):
                self._advance()
                iterables.append(self._parse_expression())
            self._consume(TokenType.KEYWORD, "Expected 'do'")
            body = self._parse_block()
            self._consume(TokenType.KEYWORD, "Expected 'end'")
            return ForInStatement(vars=vars, iterables=iterables, body=body)

    def _parse_repeat_stmt(self) -> WhileStatement:
        """Parse repeat-until statement."""
        self._consume(TokenType.KEYWORD, "Expected 'repeat'")
        body = self._parse_block()
        self._consume(TokenType.KEYWORD, "Expected 'until'")
        condition = self._parse_expression()
        # Convert repeat-until to while with negated condition
        return WhileStatement(
            condition=UnaryOp(op="not", operand=condition),
            body=body,
        )

    def _parse_return_stmt(self) -> ReturnStatement:
        """Parse return statement."""
        self._consume(TokenType.KEYWORD, "Expected 'return'")
        values = []
        if not self._is_block_end() and not self._match(TokenType.SEMICOLON):
            values.append(self._parse_expression())
            while self._match(TokenType.COMMA):
                self._advance()
                values.append(self._parse_expression())
        return ReturnStatement(values=values)

    def _parse_assignment_or_call(self) -> Optional[ASTNode]:
        """Parse assignment or function call."""
        expr = self._parse_expression()
        if self._match(TokenType.ASSIGN, TokenType.COMMA):
            targets = [expr]
            while self._match(TokenType.COMMA):
                self._advance()
                targets.append(self._parse_expression())
            self._consume(TokenType.ASSIGN)
            values = [self._parse_expression()]
            while self._match(TokenType.COMMA):
                self._advance()
                values.append(self._parse_expression())
            return Assignment(targets=targets, values=values)
        return expr

    def _parse_expression(self) -> ASTNode:
        """Parse expression."""
        return self._parse_or_expr()

    def _parse_or_expr(self) -> ASTNode:
        """Parse or expression."""
        left = self._parse_and_expr()
        while self._match(TokenType.KEYWORD) and self._current().value == "or":
            op = self._advance().value
            right = self._parse_and_expr()
            left = BinaryOp(op=op, left=left, right=right)
        return left

    def _parse_and_expr(self) -> ASTNode:
        """Parse and expression."""
        left = self._parse_comparison_expr()
        while self._match(TokenType.KEYWORD) and self._current().value == "and":
            op = self._advance().value
            right = self._parse_comparison_expr()
            left = BinaryOp(op=op, left=left, right=right)
        return left

    def _parse_comparison_expr(self) -> ASTNode:
        """Parse comparison expression."""
        left = self._parse_concat_expr()
        while self._match(
            TokenType.EQUAL,
            TokenType.NOT_EQUAL,
            TokenType.LESS,
            TokenType.GREATER,
            TokenType.LESS_EQUAL,
            TokenType.GREATER_EQUAL,
        ):
            op = self._advance().value
            right = self._parse_concat_expr()
            left = BinaryOp(op=op, left=left, right=right)
        return left

    def _parse_concat_expr(self) -> ASTNode:
        """Parse concatenation expression."""
        left = self._parse_additive_expr()
        while self._match(TokenType.CONCAT):
            op = self._advance().value
            right = self._parse_additive_expr()
            left = BinaryOp(op=op, left=left, right=right)
        return left

    def _parse_additive_expr(self) -> ASTNode:
        """Parse addition/subtraction expression."""
        left = self._parse_multiplicative_expr()
        while self._match(TokenType.PLUS, TokenType.MINUS):
            op = self._advance().value
            right = self._parse_multiplicative_expr()
            left = BinaryOp(op=op, left=left, right=right)
        return left

    def _parse_multiplicative_expr(self) -> ASTNode:
        """Parse multiplication/division expression."""
        left = self._parse_power_expr()
        while self._match(TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
            op = self._advance().value
            right = self._parse_power_expr()
            left = BinaryOp(op=op, left=left, right=right)
        return left

    def _parse_power_expr(self) -> ASTNode:
        """Parse power expression."""
        left = self._parse_unary_expr()
        if self._match(TokenType.POWER):
            op = self._advance().value
            right = self._parse_power_expr()  # Right associative
            left = BinaryOp(op=op, left=left, right=right)
        return left

    def _parse_unary_expr(self) -> ASTNode:
        """Parse unary expression."""
        if self._match(TokenType.MINUS, TokenType.LENGTH):
            op = self._advance().value
            expr = self._parse_unary_expr()
            return UnaryOp(op=op, operand=expr)
        if self._match(TokenType.KEYWORD) and self._current().value == "not":
            op = self._advance().value
            expr = self._parse_unary_expr()
            return UnaryOp(op=op, operand=expr)
        return self._parse_postfix_expr()

    def _parse_postfix_expr(self) -> ASTNode:
        """Parse postfix expression (calls, indexing, etc)."""
        expr = self._parse_primary_expr()
        while True:
            if self._match(TokenType.LPAREN):
                self._advance()
                args = []
                if not self._match(TokenType.RPAREN):
                    args.append(self._parse_expression())
                    while self._match(TokenType.COMMA):
                        self._advance()
                        args.append(self._parse_expression())
                self._consume(TokenType.RPAREN)
                expr = FunctionCall(func=expr, args=args)
            elif self._match(TokenType.LBRACKET):
                self._advance()
                index = self._parse_expression()
                self._consume(TokenType.RBRACKET)
                expr = Index(table=expr, index=index)
            elif self._match(TokenType.DOT):
                self._advance()
                prop = self._consume(TokenType.IDENTIFIER).value
                expr = Property(object=expr, property=prop)
            elif self._match(TokenType.COLON):
                self._advance()
                method = self._consume(TokenType.IDENTIFIER).value
                self._consume(TokenType.LPAREN)
                args = []
                if not self._match(TokenType.RPAREN):
                    args.append(self._parse_expression())
                    while self._match(TokenType.COMMA):
                        self._advance()
                        args.append(self._parse_expression())
                self._consume(TokenType.RPAREN)
                # Method call: obj:method(args) -> obj.method(obj, args)
                method_ref = Property(object=expr, property=method)
                expr = FunctionCall(func=method_ref, args=[expr] + args)
            else:
                break
        return expr

    def _parse_primary_expr(self) -> ASTNode:
        """Parse primary expression."""
        # Number
        if self._match(TokenType.NUMBER):
            value = self._advance().value
            return NumberLiteral(value=value)

        # String
        if self._match(TokenType.STRING):
            value = self._advance().value
            return StringLiteral(value=value)

        # Boolean
        if self._match(TokenType.KEYWORD):
            if self._current().value == "true":
                self._advance()
                return BooleanLiteral(value=True)
            elif self._current().value == "false":
                self._advance()
                return BooleanLiteral(value=False)
            elif self._current().value == "nil":
                self._advance()
                return NilLiteral()

        # Identifier
        if self._match(TokenType.IDENTIFIER):
            name = self._advance().value
            return Identifier(name=name)

        # Parenthesized expression
        if self._match(TokenType.LPAREN):
            self._advance()
            expr = self._parse_expression()
            self._consume(TokenType.RPAREN)
            return expr

        # Table constructor
        if self._match(TokenType.LBRACE):
            return self._parse_table_constructor()

        # Function expression
        if self._match(TokenType.KEYWORD) and self._current().value == "function":
            self._advance()
            self._consume(TokenType.LPAREN)
            params, vararg = self._parse_params()
            self._consume(TokenType.RPAREN)
            body = self._parse_block()
            self._consume(TokenType.KEYWORD, "Expected 'end'")
            return FunctionExpression(params=params, vararg=vararg, body=body)

        raise SyntaxError(f"Unexpected token: {self._current()}")

    def _parse_table_constructor(self) -> TableConstructor:
        """Parse table constructor."""
        self._consume(TokenType.LBRACE)
        fields = []

        while not self._match(TokenType.RBRACE):
            if self._match(TokenType.LBRACKET):
                # [expr] = value
                self._advance()
                key = self._parse_expression()
                self._consume(TokenType.RBRACKET)
                self._consume(TokenType.ASSIGN)
                value = self._parse_expression()
                fields.append((key, value))
            elif self._match(TokenType.IDENTIFIER) and self._peek() and self._peek().type == TokenType.ASSIGN:
                # key = value
                key = Identifier(name=self._advance().value)
                self._consume(TokenType.ASSIGN)
                value = self._parse_expression()
                fields.append((key, value))
            else:
                # Just value
                value = self._parse_expression()
                fields.append((None, value))

            if not self._match(TokenType.RBRACE):
                if self._match(TokenType.COMMA):
                    self._advance()
                elif self._match(TokenType.SEMICOLON):
                    self._advance()

        self._consume(TokenType.RBRACE)
        return TableConstructor(fields=fields)
