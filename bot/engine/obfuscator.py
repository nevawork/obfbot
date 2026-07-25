"""Main obfuscation engine orchestrator."""

import time
from typing import Optional, Dict, Any, Tuple
from bot.engine.parser import Parser
from bot.engine.output import CodeGenerator
from bot.engine.identifier_protection import IdentifierProtection
from bot.engine.string_protection import StringProtection
from bot.engine.number_protection import NumberProtection
from bot.engine.controlflow import ControlFlowProtection
from bot.engine.settings import ObfuscationSettings
from bot.logger import logger


class ObfuscationEngine:
    """Main obfuscation engine."""

    def __init__(self, settings: Optional[ObfuscationSettings] = None):
        """Initialize obfuscation engine.

        Args:
            settings: Obfuscation settings
        """
        self.settings = settings or ObfuscationSettings()
        self.statistics = {}

    def obfuscate(self, code: str) -> Tuple[str, Dict[str, Any]]:
        """Obfuscate Lua code.

        Args:
            code: Lua code to obfuscate

        Returns:
            Tuple of (obfuscated_code, statistics)
        """
        start_time = time.time()
        try:
            # Parse code to AST
            logger.info("Parsing code...")
            parser = Parser.from_code(code)
            ast = parser.parse()

            # Apply protections
            ast = self._apply_protections(ast)

            # Generate code
            logger.info("Generating output code...")
            generator = CodeGenerator(
                minify=self.settings.output_formatting == "minified"
            )
            obfuscated = generator.generate(ast)

            # Calculate statistics
            elapsed = time.time() - start_time
            stats = self._calculate_statistics(code, obfuscated, elapsed)

            logger.info(f"Obfuscation completed in {elapsed:.2f}s")
            return obfuscated, stats

        except Exception as e:
            logger.error(f"Obfuscation failed: {e}")
            raise

    def _apply_protections(self, ast) -> Any:
        """Apply all protection modules.

        Args:
            ast: AST to protect

        Returns:
            Protected AST
        """
        seed = self.settings.random_seed

        # Identifier Protection
        if self.settings.rename_variables or self.settings.rename_functions:
            logger.info("Applying identifier protection...")
            identifier_prot = IdentifierProtection(seed=seed)
            ast = identifier_prot.protect(
                ast,
                rename_vars=self.settings.rename_variables
            )

        # String Protection
        if self.settings.encrypt_strings:
            logger.info("Applying string protection...")
            string_prot = StringProtection(seed=seed)
            ast = string_prot.protect(
                ast,
                encrypt=True,
                split=self.settings.string_split
            )

        # Number Protection
        if self.settings.encode_constants:
            logger.info("Applying number protection...")
            number_prot = NumberProtection(seed=seed)
            ast = number_prot.protect(ast, encode=True)

        # Control Flow Protection
        if self.settings.flatten_control_flow or self.settings.insert_dead_code:
            logger.info("Applying control flow protection...")
            cf_prot = ControlFlowProtection(seed=seed)
            ast = cf_prot.protect(
                ast,
                flatten=self.settings.flatten_control_flow,
                dead_code_amount=self.settings.dead_code_amount
            )

        return ast

    def _calculate_statistics(self, original: str, obfuscated: str, elapsed: float) -> Dict[str, Any]:
        """Calculate obfuscation statistics.

        Args:
            original: Original code
            obfuscated: Obfuscated code
            elapsed: Time elapsed

        Returns:
            Statistics dictionary
        """
        return {
            "original_size": len(original),
            "obfuscated_size": len(obfuscated),
            "size_ratio": len(obfuscated) / len(original) if original else 1.0,
            "processing_time": elapsed,
            "identifiers_renamed": self._count_identifiers(original),
            "strings_encrypted": self.settings.encrypt_strings,
            "numbers_encoded": self.settings.encode_constants,
            "control_flow_flattened": self.settings.flatten_control_flow,
            "dead_code_inserted": self.settings.insert_dead_code,
            "protection_summary": self._generate_summary(),
        }

    def _count_identifiers(self, code: str) -> int:
        """Count identifiers in code."""
        # Simplified counting
        import re
        identifiers = re.findall(r"\b[a-zA-Z_][a-zA-Z0-9_]*\b", code)
        return len(set(identifiers))

    def _generate_summary(self) -> str:
        """Generate protection summary."""
        protections = []
        if self.settings.rename_variables:
            protections.append("Variable renaming")
        if self.settings.encrypt_strings:
            protections.append("String encryption")
        if self.settings.encode_constants:
            protections.append("Number encoding")
        if self.settings.flatten_control_flow:
            protections.append("Control flow flattening")
        if self.settings.insert_dead_code:
            protections.append(f"Dead code ({self.settings.dead_code_amount})")
        if self.settings.anti_debug:
            protections.append("Anti-debug")
        if self.settings.integrity_check:
            protections.append("Integrity check")
        return ", ".join(protections) if protections else "None"
