"""Parser tests."""

import pytest
from bot.engine.tokenizer import Tokenizer
from bot.engine.parser import Parser
from bot.engine.ast import NodeType


def test_tokenizer_basic():
    """Test tokenizer with basic code."""
    code = "local x = 42"
    tokenizer = Tokenizer(code)
    tokens = tokenizer.tokenize()
    assert len(tokens) > 0
    assert tokens[0].value == "local"


def test_parser_basic():
    """Test parser with basic code."""
    code = "local x = 42"
    parser = Parser.from_code(code)
    ast = parser.parse()
    assert ast.type == NodeType.BLOCK
    assert len(ast.statements) > 0


def test_parser_function():
    """Test parser with function."""
    code = """
    function add(a, b)
        return a + b
    end
    """
    parser = Parser.from_code(code)
    ast = parser.parse()
    assert ast.type == NodeType.BLOCK


def test_parser_table():
    """Test parser with table."""
    code = """
    local t = {x = 1, y = 2}
    """
    parser = Parser.from_code(code)
    ast = parser.parse()
    assert ast.type == NodeType.BLOCK
