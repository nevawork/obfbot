"""Number protection - arithmetic encoding and constant obfuscation."""

import random
from typing import Optional
from bot.engine.ast import (
    ASTNode,
    NumberLiteral,
    BinaryOp,
    Identifier,
)


class NumberProtection:
    """Encode numbers and constants."""

    def __init__(self, seed: Optional[int] = None):
        """Initialize number protection.

        Args:
            seed: Random seed
        """
        if seed is not None:
            random.seed(seed)
        self.constant_map = {}  # original -> encoded expression

    def protect(self, node: ASTNode, encode: bool = True) -> ASTNode:
        """Protect numbers in AST.

        Args:
            node: AST node
            encode: Whether to encode numbers

        Returns:
            Protected AST
        """
        if not encode:
            return node
        return self._process_node(node)

    def _process_node(self, node: ASTNode) -> ASTNode:
        """Process node recursively."""
        if isinstance(node, NumberLiteral):
            # Encode number
            return self._encode_number(node.value)

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

    def _encode_number(self, num_str: str) -> ASTNode:
        """Encode number using arithmetic operations.

        Args:
            num_str: Number as string

        Returns:
            Encoded AST node
        """
        try:
            num = float(num_str) if '.' in num_str else int(num_str)
        except ValueError:
            return NumberLiteral(value=num_str)

        # Choose random encoding method
        method = random.choice(["add", "multiply", "xor", "subtract"])

        if method == "add":
            # a + b = c
            a = int(num / 2) if isinstance(num, int) else num / 2
            b = num - a
            return BinaryOp(
                op="+",
                left=NumberLiteral(value=str(a)),
                right=NumberLiteral(value=str(b)),
            )
        elif method == "multiply":
            # a * b = c (for non-zero)
            if num != 0:
                a = random.randint(1, 10)
                b = int(num / a) if num % a == 0 else num / a
                return BinaryOp(
                    op="*",
                    left=NumberLiteral(value=str(a)),
                    right=NumberLiteral(value=str(b)),
                )
        elif method == "subtract":
            # a - b = c
            offset = random.randint(1, 100)
            a = num + offset
            return BinaryOp(
                op="-",
                left=NumberLiteral(value=str(a)),
                right=NumberLiteral(value=str(offset)),
            )

        return NumberLiteral(value=num_str)
