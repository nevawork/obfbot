"""Identifier protection - variable and function renaming."""

import string
import random
from typing import Dict, Set, Optional
from bot.engine.ast import (
    ASTNode,
    Block,
    LocalAssignment,
    FunctionDef,
    Identifier,
    Property,
    FunctionCall,
    Index,
)


class IdentifierProtection:
    """Rename identifiers to obfuscate code."""

    # Reserved Lua keywords that cannot be used as identifiers
    RESERVED = {
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

    # Common library names to preserve
    PRESERVE = {
        "print",
        "pairs",
        "ipairs",
        "type",
        "tostring",
        "tonumber",
        "math",
        "string",
        "table",
        "os",
        "io",
        "debug",
        "error",
        "pcall",
        "xpcall",
        "coroutine",
        "require",
        "module",
        "assert",
        "next",
        "rawget",
        "rawset",
        "getmetatable",
        "setmetatable",
        "rawequal",
        "select",
        "unpack",
    }

    def __init__(self, seed: Optional[int] = None):
        """Initialize identifier protection.

        Args:
            seed: Random seed for reproducibility
        """
        if seed is not None:
            random.seed(seed)
        self.rename_map: Dict[str, str] = {}  # original -> renamed
        self.scope_stack: list = [set()]  # Stack of scope variables
        self.counter = 0

    def protect(self, node: ASTNode, rename_vars: bool = True) -> ASTNode:
        """Protect identifiers in AST.

        Args:
            node: AST node to protect
            rename_vars: Whether to rename variables

        Returns:
            Protected AST
        """
        if not rename_vars:
            return node
        return self._process_node(node)

    def _process_node(self, node: ASTNode) -> ASTNode:
        """Process node recursively."""
        if isinstance(node, Block):
            self.scope_stack.append(set())
            node.statements = [self._process_node(stmt) for stmt in node.statements]
            self.scope_stack.pop()
            return node

        elif isinstance(node, LocalAssignment):
            # Register local variables
            for name in node.names:
                renamed = self._generate_name()
                self.rename_map[name] = renamed
                self.scope_stack[-1].add(name)
            node.names = [self.rename_map.get(name, name) for name in node.names]
            node.values = [self._process_node(val) for val in node.values]
            return node

        elif isinstance(node, FunctionDef):
            # Rename function
            if node.name not in self.PRESERVE:
                node.name = self._generate_name()
            
            # Process parameters
            self.scope_stack.append(set())
            for param in node.params:
                renamed = self._generate_name()
                self.rename_map[param] = renamed
                self.scope_stack[-1].add(param)
            node.params = [self.rename_map.get(param, param) for param in node.params]
            
            # Process body
            node.body = self._process_node(node.body)
            self.scope_stack.pop()
            return node

        elif isinstance(node, Identifier):
            # Rename identifier if mapped
            if node.name in self.rename_map:
                node.name = self.rename_map[node.name]
            return node

        elif isinstance(node, Property):
            # Don't rename properties (table keys stay the same)
            node.object = self._process_node(node.object)
            return node

        elif hasattr(node, "__dict__"):
            # Process all child nodes
            for key, value in node.__dict__.items():
                if isinstance(value, ASTNode):
                    node.__dict__[key] = self._process_node(value)
                elif isinstance(value, list):
                    node.__dict__[key] = [
                        self._process_node(item) if isinstance(item, ASTNode) else item
                        for item in value
                    ]
                elif isinstance(value, tuple):
                    node.__dict__[key] = tuple(
                        self._process_node(item) if isinstance(item, ASTNode) else item
                        for item in value
                    )
            return node

        return node

    def _generate_name(self, length: int = 8) -> str:
        """Generate random identifier name.

        Args:
            length: Length of name

        Returns:
            Random identifier
        """
        while True:
            # Generate name with mix of letters (avoid confusion)
            name = "".join(random.choices(string.ascii_letters, k=length))
            # Ensure it's not in reserved or already used
            if name not in self.RESERVED and name not in self.rename_map.values():
                return name
