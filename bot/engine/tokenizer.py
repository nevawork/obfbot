"""Tokenizer for Lua/Luau code."""

from typing import List, Optional
from enum import Enum
from dataclasses import dataclass


class TokenType(str, Enum):
    """Token types."""

    # Literals
    NUMBER = "number"
    STRING = "string"
    IDENTIFIER = "identifier"
    KEYWORD = "keyword"

    # Operators
    PLUS = "plus"
    MINUS = "minus"
    MULTIPLY = "multiply"
    DIVIDE = "divide"
    MODULO = "modulo"
    POWER = "power"
    EQUAL = "equal"
    NOT_EQUAL = "not_equal"
    LESS = "less"
    GREATER = "greater"
    LESS_EQUAL = "less_equal"
    GREATER_EQUAL = "greater_equal"
    ASSIGN = "assign"
    CONCAT = "concat"
    LENGTH = "length"

    # Delimiters
    LPAREN = "lparen"
    RPAREN = "rparen"
    LBRACE = "lbrace"
    RBRACE = "rbrace"
    LBRACKET = "lbracket"
    RBRACKET = "rbracket"
    COMMA = "comma"
    DOT = "dot"
    COLON = "colon"
    SEMICOLON = "semicolon"

    # Special
    EOF = "eof"
    NEWLINE = "newline"
    COMMENT = "comment"


@dataclass
class Token:
    """Represents a token."""

    type: TokenType
    value: str
    line: int
    column: int

    def __repr__(self) -> str:
        return f"Token({self.type}, {repr(self.value)}, {self.line}:{self.column})"


class Tokenizer:
    """Tokenizes Lua/Luau code."""

    KEYWORDS = {
        "and",
        "break",
        "do",
        "else",
        "elseif",
        "end",
        "false",
        "for",
        "function",
        "if",
        "in",
        "local",
        "nil",
        "not",
        "or",
        "repeat",
        "return",
        "then",
        "true",
        "until",
        "while",
    }

    def __init__(self, code: str):
        """Initialize tokenizer.

        Args:
            code: Lua code to tokenize
        """
        self.code = code
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []

    def tokenize(self) -> List[Token]:
        """Tokenize code.

        Returns:
            List of tokens
        """
        while self.pos < len(self.code):
            self._skip_whitespace()
            if self.pos >= len(self.code):
                break

            char = self.code[self.pos]

            # Comments
            if char == "-" and self.peek() == "-":
                self._read_comment()
            # Strings
            elif char in ('"', "'"):
                self._read_string()
            # Numbers
            elif char.isdigit():
                self._read_number()
            # Identifiers and keywords
            elif char.isalpha() or char == "_":
                self._read_identifier()
            # Operators and delimiters
            else:
                self._read_operator()

        self.tokens.append(Token(TokenType.EOF, "", self.line, self.column))
        return self.tokens

    def _skip_whitespace(self) -> None:
        """Skip whitespace."""
        while self.pos < len(self.code) and self.code[self.pos] in " \t\r\n":
            if self.code[self.pos] == "\n":
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.pos += 1

    def _read_comment(self) -> None:
        """Read comment."""
        start_col = self.column
        comment = ""
        while self.pos < len(self.code) and self.code[self.pos] != "\n":
            comment += self.code[self.pos]
            self.pos += 1
            self.column += 1
        self.tokens.append(Token(TokenType.COMMENT, comment, self.line, start_col))

    def _read_string(self) -> None:
        """Read string literal."""
        start_col = self.column
        quote = self.code[self.pos]
        self.pos += 1
        self.column += 1
        value = ""

        while self.pos < len(self.code) and self.code[self.pos] != quote:
            if self.code[self.pos] == "\\":
                value += self.code[self.pos]
                self.pos += 1
                self.column += 1
                if self.pos < len(self.code):
                    value += self.code[self.pos]
                    self.pos += 1
                    self.column += 1
            else:
                value += self.code[self.pos]
                self.pos += 1
                self.column += 1

        if self.pos < len(self.code):
            self.pos += 1
            self.column += 1

        self.tokens.append(Token(TokenType.STRING, value, self.line, start_col))

    def _read_number(self) -> None:
        """Read number literal."""
        start_col = self.column
        value = ""

        while self.pos < len(self.code) and (self.code[self.pos].isdigit() or self.code[self.pos] == "."):
            value += self.code[self.pos]
            self.pos += 1
            self.column += 1

        # Handle scientific notation
        if self.pos < len(self.code) and self.code[self.pos] in "eE":
            value += self.code[self.pos]
            self.pos += 1
            self.column += 1
            if self.pos < len(self.code) and self.code[self.pos] in "+-":
                value += self.code[self.pos]
                self.pos += 1
                self.column += 1
            while self.pos < len(self.code) and self.code[self.pos].isdigit():
                value += self.code[self.pos]
                self.pos += 1
                self.column += 1

        self.tokens.append(Token(TokenType.NUMBER, value, self.line, start_col))

    def _read_identifier(self) -> None:
        """Read identifier or keyword."""
        start_col = self.column
        value = ""

        while self.pos < len(self.code) and (
            self.code[self.pos].isalnum() or self.code[self.pos] == "_"
        ):
            value += self.code[self.pos]
            self.pos += 1
            self.column += 1

        if value in self.KEYWORDS:
            self.tokens.append(Token(TokenType.KEYWORD, value, self.line, start_col))
        else:
            self.tokens.append(Token(TokenType.IDENTIFIER, value, self.line, start_col))

    def _read_operator(self) -> None:
        """Read operator or delimiter."""
        start_col = self.column
        char = self.code[self.pos]
        next_char = self.peek()
        two_char = char + (next_char or "")

        # Two-character operators
        if two_char == "==":
            self.tokens.append(Token(TokenType.EQUAL, two_char, self.line, start_col))
            self.pos += 2
            self.column += 2
        elif two_char == "~=":
            self.tokens.append(Token(TokenType.NOT_EQUAL, two_char, self.line, start_col))
            self.pos += 2
            self.column += 2
        elif two_char == "<=":
            self.tokens.append(Token(TokenType.LESS_EQUAL, two_char, self.line, start_col))
            self.pos += 2
            self.column += 2
        elif two_char == ">=":
            self.tokens.append(Token(TokenType.GREATER_EQUAL, two_char, self.line, start_col))
            self.pos += 2
            self.column += 2
        elif two_char == "..": 
            self.tokens.append(Token(TokenType.CONCAT, two_char, self.line, start_col))
            self.pos += 2
            self.column += 2
        # Single-character operators
        elif char == "+":
            self.tokens.append(Token(TokenType.PLUS, char, self.line, start_col))
            self.pos += 1
            self.column += 1
        elif char == "-":
            self.tokens.append(Token(TokenType.MINUS, char, self.line, start_col))
            self.pos += 1
            self.column += 1
        elif char == "*":
            self.tokens.append(Token(TokenType.MULTIPLY, char, self.line, start_col))
            self.pos += 1
            self.column += 1
        elif char == "/":
            self.tokens.append(Token(TokenType.DIVIDE, char, self.line, start_col))
            self.pos += 1
            self.column += 1
        elif char == "%":
            self.tokens.append(Token(TokenType.MODULO, char, self.line, start_col))
            self.pos += 1
            self.column += 1
        elif char == "^":
            self.tokens.append(Token(TokenType.POWER, char, self.line, start_col))
            self.pos += 1
            self.column += 1
        elif char == "=":
            self.tokens.append(Token(TokenType.ASSIGN, char, self.line, start_col))
            self.pos += 1
            self.column += 1
        elif char == "#":
            self.tokens.append(Token(TokenType.LENGTH, char, self.line, start_col))
            self.pos += 1
            self.column += 1
        elif char == "<":
            self.tokens.append(Token(TokenType.LESS, char, self.line, start_col))
            self.pos += 1
            self.column += 1
        elif char == ">":
            self.tokens.append(Token(TokenType.GREATER, char, self.line, start_col))
            self.pos += 1
            self.column += 1
        elif char == "(":
            self.tokens.append(Token(TokenType.LPAREN, char, self.line, start_col))
            self.pos += 1
            self.column += 1
        elif char == ")":
            self.tokens.append(Token(TokenType.RPAREN, char, self.line, start_col))
            self.pos += 1
            self.column += 1
        elif char == "{":
            self.tokens.append(Token(TokenType.LBRACE, char, self.line, start_col))
            self.pos += 1
            self.column += 1
        elif char == "}":
            self.tokens.append(Token(TokenType.RBRACE, char, self.line, start_col))
            self.pos += 1
            self.column += 1
        elif char == "[":
            self.tokens.append(Token(TokenType.LBRACKET, char, self.line, start_col))
            self.pos += 1
            self.column += 1
        elif char == "]":
            self.tokens.append(Token(TokenType.RBRACKET, char, self.line, start_col))
            self.pos += 1
            self.column += 1
        elif char == ",":
            self.tokens.append(Token(TokenType.COMMA, char, self.line, start_col))
            self.pos += 1
            self.column += 1
        elif char == ".":
            self.tokens.append(Token(TokenType.DOT, char, self.line, start_col))
            self.pos += 1
            self.column += 1
        elif char == ":":
            self.tokens.append(Token(TokenType.COLON, char, self.line, start_col))
            self.pos += 1
            self.column += 1
        elif char == ";":
            self.tokens.append(Token(TokenType.SEMICOLON, char, self.line, start_col))
            self.pos += 1
            self.column += 1
        else:
            # Unknown character, skip
            self.pos += 1
            self.column += 1

    def peek(self, offset: int = 1) -> Optional[str]:
        """Peek at character ahead.

        Args:
            offset: How many characters ahead

        Returns:
            Character or None
        """
        pos = self.pos + offset
        return self.code[pos] if pos < len(self.code) else None
