"""Randomization utilities."""

import random
import string
from typing import Optional


class Randomizer:
    """Handle randomization for obfuscation."""

    def __init__(self, seed: Optional[int] = None):
        """Initialize randomizer.

        Args:
            seed: Random seed for reproducibility
        """
        if seed is not None:
            random.seed(seed)
        self.seed = seed

    @staticmethod
    def random_identifier(length: int = 8) -> str:
        """Generate random identifier.

        Args:
            length: Length of identifier

        Returns:
            Random identifier
        """
        return "".join(random.choices(string.ascii_letters, k=length))

    @staticmethod
    def random_hex_key(length: int = 32) -> str:
        """Generate random hex key.

        Args:
            length: Length of key

        Returns:
            Random hex string
        """
        return "".join(random.choices(string.hexdigits[:16], k=length))

    @staticmethod
    def random_seed() -> int:
        """Generate random seed.

        Returns:
            Random seed
        """
        return random.randint(0, 2**31 - 1)

    @staticmethod
    def shuffle_list(lst: list) -> list:
        """Shuffle list.

        Args:
            lst: List to shuffle

        Returns:
            Shuffled list
        """
        shuffled = lst.copy()
        random.shuffle(shuffled)
        return shuffled
