"""Obfuscation engine tests."""

import pytest
from bot.engine.obfuscator import ObfuscationEngine
from bot.engine.settings import ObfuscationSettings


def test_obfuscate_simple():
    """Test simple obfuscation."""
    code = "local x = 42"
    settings = ObfuscationSettings(obfuscation_level=5)
    engine = ObfuscationEngine(settings)
    obfuscated, stats = engine.obfuscate(code)
    assert obfuscated is not None
    assert stats["original_size"] > 0


def test_obfuscation_levels():
    """Test different obfuscation levels."""
    code = "local x = 42\nlocal y = 43"
    
    for level in range(1, 11):
        settings = ObfuscationSettings(obfuscation_level=level)
        engine = ObfuscationEngine(settings)
        obfuscated, stats = engine.obfuscate(code)
        assert obfuscated is not None
        assert stats["obfuscation_level"] == level


def test_obfuscation_with_function():
    """Test obfuscation with function."""
    code = """
    local function greet(name)
        print("Hello, " .. name)
    end
    """
    settings = ObfuscationSettings(obfuscation_level=5)
    engine = ObfuscationEngine(settings)
    obfuscated, stats = engine.obfuscate(code)
    assert obfuscated is not None
