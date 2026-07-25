"""String protection - encryption and obfuscation."""

import random
import string
from typing import Dict, List, Optional
from base64 import b64encode
from bot.engine.ast import (
    ASTNode,
    StringLiteral,
    Block,
    BinaryOp,
    UnaryOp,
    FunctionCall,
    Index,
)


class StringProtection:
    """Encrypt and obfuscate strings."""

    def __init__(self, seed: Optional[int] = None):
        """Initialize string protection.

        Args:
            seed: Random seed
        """
        if seed is not None:
            random.seed(seed)
        self.string_map: Dict[str, str] = {}  # original -> encrypted key
        self.encryption_key = "".join(random.choices(string.ascii_letters + string.digits, k=32))

    def protect(self, node: ASTNode, encrypt: bool = True, split: bool = False) -> ASTNode:
        """Protect strings in AST.

        Args:
            node: AST node
            encrypt: Whether to encrypt strings
            split: Whether to split strings

        Returns:
            Protected AST
        """
        if not encrypt:
            return node
        return self._process_node(node, split)

    def _process_node(self, node: ASTNode, split: bool = False) -> ASTNode:
        """Process node recursively."""
        if isinstance(node, StringLiteral):
            # Encrypt string
            encrypted = self._encrypt_string(node.value)
            # Replace with runtime decryption call
            return self._create_decrypt_call(encrypted, split)

        elif hasattr(node, "__dict__"):
            # Process all child nodes
            for key, value in node.__dict__.items():
                if isinstance(value, ASTNode):
                    node.__dict__[key] = self._process_node(value, split)
                elif isinstance(value, list):
                    node.__dict__[key] = [
                        self._process_node(item, split) if isinstance(item, ASTNode) else item
                        for item in value
                    ]
                elif isinstance(value, tuple):
                    node.__dict__[key] = tuple(
                        self._process_node(item, split) if isinstance(item, ASTNode) else item
                        for item in value
                    )
            return node

        return node

    def _encrypt_string(self, s: str) -> str:
        """Encrypt string with XOR.

        Args:
            s: String to encrypt

        Returns:
            Encrypted hex string
        """
        encrypted = bytearray()
        key_bytes = self.encryption_key.encode()
        for i, char in enumerate(s.encode()):
            encrypted.append(char ^ key_bytes[i % len(key_bytes)])
        return encrypted.hex()

    def _create_decrypt_call(self, encrypted: str, split: bool = False) -> ASTNode:
        """Create runtime decryption function call.

        Args:
            encrypted: Encrypted string
            split: Whether to split string

        Returns:
            FunctionCall AST node
        """
        # For now, return a simple representation
        # In full implementation, this would create actual AST nodes
        from bot.engine.ast import Identifier, StringLiteral
        
        return FunctionCall(
            func=Identifier(name="__decrypt_string"),
            args=[
                StringLiteral(value=encrypted),
                StringLiteral(value=self.encryption_key),
            ],
        )

    def get_runtime_code(self) -> str:
        """Get runtime decryption code.

        Returns:
            Lua code for decryption
        """
        return '''
local __encryption_key = {key_placeholder}

local function __decrypt_string(encrypted_hex, key)
    local result = ""
    local key_bytes = {{key:byte(1, -1)}}
    for i = 1, #encrypted_hex, 2 do
        local byte_val = tonumber(encrypted_hex:sub(i, i+1), 16)
        result = result .. string.char(byte_val ~ key_bytes[((i//2 - 1) % #key_bytes) + 1])
    end
    return result
end
'''.format(key_placeholder=repr(self.encryption_key))
