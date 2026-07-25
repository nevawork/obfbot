"""Obfuscation settings and options."""

from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class ObfuscationSettings:
    """Obfuscation configuration."""

    # General
    obfuscation_level: int = 5  # 1-10
    random_seed: int = None  # None = random

    # Identifier Protection
    rename_variables: bool = True
    rename_functions: bool = True
    scope_aware_renaming: bool = True

    # String Protection
    encrypt_strings: bool = True
    string_split: bool = False
    string_randomize_keys: bool = True

    # Number Protection
    encode_constants: bool = True
    arithmetic_encoding: bool = True

    # Control Flow
    flatten_control_flow: bool = False
    insert_dead_code: bool = True
    dead_code_amount: int = 5  # 0-10
    opaque_predicates: bool = True
    bogus_branches: bool = True

    # Table Protection
    hide_table_keys: bool = True
    proxy_tables: bool = False

    # Function Protection
    wrap_functions: bool = True
    indirect_calls: bool = False

    # Anti-Tamper
    integrity_check: bool = True
    modification_detection: bool = True

    # Anti-Debug
    anti_debug: bool = False
    environment_validation: bool = False

    # Output
    output_formatting: str = "minified"  # minified or formatted
    compress_output: bool = False
    include_statistics: bool = True

    # Advanced
    preserve_comments: bool = False
    extra_options: Dict[str, Any] = field(default_factory=dict)

    def apply_level(self, level: int) -> None:
        """Apply obfuscation level preset.

        Args:
            level: Obfuscation level (1-10)
        """
        self.obfuscation_level = max(1, min(10, level))

        if level <= 2:
            # Light obfuscation
            self.rename_variables = True
            self.encrypt_strings = False
            self.encode_constants = False
            self.flatten_control_flow = False
            self.insert_dead_code = False
        elif level <= 4:
            # Moderate obfuscation
            self.rename_variables = True
            self.encrypt_strings = True
            self.encode_constants = False
            self.flatten_control_flow = False
            self.insert_dead_code = True
            self.dead_code_amount = 3
        elif level <= 6:
            # Heavy obfuscation
            self.rename_variables = True
            self.encrypt_strings = True
            self.encode_constants = True
            self.flatten_control_flow = False
            self.insert_dead_code = True
            self.dead_code_amount = 5
            self.anti_debug = True
        elif level <= 8:
            # Very heavy obfuscation
            self.rename_variables = True
            self.encrypt_strings = True
            self.encode_constants = True
            self.flatten_control_flow = True
            self.insert_dead_code = True
            self.dead_code_amount = 7
            self.anti_debug = True
            self.integrity_check = True
        else:
            # Maximum obfuscation
            self.rename_variables = True
            self.encrypt_strings = True
            self.encode_constants = True
            self.flatten_control_flow = True
            self.insert_dead_code = True
            self.dead_code_amount = 10
            self.anti_debug = True
            self.integrity_check = True
            self.modification_detection = True
            self.environment_validation = True

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary.

        Returns:
            Settings as dictionary
        """
        return {
            "obfuscation_level": self.obfuscation_level,
            "random_seed": self.random_seed,
            "rename_variables": self.rename_variables,
            "encrypt_strings": self.encrypt_strings,
            "encode_constants": self.encode_constants,
            "flatten_control_flow": self.flatten_control_flow,
            "dead_code_amount": self.dead_code_amount,
            "anti_debug": self.anti_debug,
        }
