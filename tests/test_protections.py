"""Protection modules tests."""

import pytest
from bot.engine.identifier_protection import IdentifierProtection
from bot.engine.string_protection import StringProtection
from bot.engine.number_protection import NumberProtection
from bot.engine.ast import (
    LocalAssignment,
    StringLiteral,
    NumberLiteral,
    Identifier,
)


def test_identifier_protection():
    """Test identifier protection."""
    prot = IdentifierProtection(seed=42)
    local_assign = LocalAssignment(
        names=["my_var"],
        values=[NumberLiteral(value="42")],
    )
    result = prot.protect(local_assign)
    assert result is not None
    # Variable name should be renamed
    assert result.names[0] != "my_var"


def test_string_protection():
    """Test string protection."""
    prot = StringProtection(seed=42)
    string_lit = StringLiteral(value="Hello, World!")
    result = prot.protect(string_lit)
    assert result is not None


def test_number_protection():
    """Test number protection."""
    prot = NumberProtection(seed=42)
    number_lit = NumberLiteral(value="42")
    result = prot.protect(number_lit)
    assert result is not None
