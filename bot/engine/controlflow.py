"""Control flow protection - flattening and dead code insertion."""

import random
from typing import Optional, Dict, List
from bot.engine.ast import (
    ASTNode,
    Block,
    IfStatement,
    WhileStatement,
    ForStatement,
    BinaryOp,
    NumberLiteral,
    BooleanLiteral,
)


class ControlFlowProtection:
    """Protect control flow through flattening and dead code."""

    def __init__(self, seed: Optional[int] = None):
        """Initialize control flow protection.

        Args:
            seed: Random seed
        """
        if seed is not None:
            random.seed(seed)
        self.counter = 0

    def protect(
        self,
        node: ASTNode,
        flatten: bool = False,
        dead_code_amount: int = 5,
    ) -> ASTNode:
        """Protect control flow.

        Args:
            node: AST node
            flatten: Whether to flatten control flow
            dead_code_amount: Amount of dead code to insert (0-10)

        Returns:
            Protected AST
        """
        node = self._insert_dead_code(node, dead_code_amount)
        if flatten:
            node = self._flatten_control_flow(node)
        return node

    def _insert_dead_code(self, node: ASTNode, amount: int = 5) -> ASTNode:
        """Insert dead code into block.

        Args:
            node: AST node
            amount: Amount of dead code to insert

        Returns:
            Modified AST
        """
        if not isinstance(node, Block):
            return node

        # Add dead code statements
        amount = min(max(amount, 0), 10)
        for _ in range(amount):
            dead_stmt = self._generate_dead_code()
            # Insert at random position
            pos = random.randint(0, len(node.statements))
            node.statements.insert(pos, dead_stmt)

        # Process child blocks
        node.statements = [self._insert_dead_code(stmt, amount) for stmt in node.statements]
        return node

    def _generate_dead_code(self) -> ASTNode:
        """Generate dead code statement.

        Returns:
            Dead code AST node
        """
        # Generate unreachable code
        choice = random.choice(["if_false", "loop_zero"])

        if choice == "if_false":
            # if false then ... end
            return IfStatement(
                condition=BooleanLiteral(value=False),
                then_block=Block(statements=[]),
            )
        else:
            # while false do ... end
            return WhileStatement(
                condition=BooleanLiteral(value=False),
                body=Block(statements=[]),
            )

    def _flatten_control_flow(self, node: ASTNode) -> ASTNode:
        """Flatten control flow structures.

        Args:
            node: AST node

        Returns:
            Flattened AST
        """
        # This is a simplified version
        # Full implementation would convert to state machine
        if isinstance(node, IfStatement):
            # Convert nested ifs to sequence
            return self._flatten_if_statement(node)
        elif isinstance(node, Block):
            node.statements = [self._flatten_control_flow(stmt) for stmt in node.statements]
        elif hasattr(node, "__dict__"):
            for key, value in node.__dict__.items():
                if isinstance(value, ASTNode):
                    node.__dict__[key] = self._flatten_control_flow(value)
                elif isinstance(value, list):
                    node.__dict__[key] = [
                        self._flatten_control_flow(item) if isinstance(item, ASTNode) else item
                        for item in value
                    ]
        return node

    def _flatten_if_statement(self, node: IfStatement) -> ASTNode:
        """Flatten if statement.

        Args:
            node: If statement

        Returns:
            Flattened AST
        """
        # Keep structure for now (full implementation would flatten to dispatcher)
        return node
