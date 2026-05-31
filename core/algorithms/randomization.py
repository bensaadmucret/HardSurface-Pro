# HardSurface Pro - Procedural Hard-Surface Generation Addon for Blender
# Copyright (C) 2024 HardSurface Pro Contributors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

"""
Randomization algorithms for procedural generation.
Provides seeded random operations for reproducible results.
"""

import random
from typing import List, Callable
from ...utils.math_utils import MathUtils


class Randomization:
    """Seeded randomization utilities."""
    
    def __init__(self, seed: int):
        """Initialize with a specific seed for reproducibility."""
        self.rng = random.Random(seed)
        self.seed = seed
    
    def random_float(self, min_val: float, max_val: float) -> float:
        """Get a random float between min and max."""
        return MathUtils.random_range(min_val, max_val, self.rng)
    
    def random_int(self, min_val: int, max_val: int) -> int:
        """Get a random integer between min and max."""
        return MathUtils.random_int_range(min_val, max_val, self.rng)
    
    def random_bool(self, probability: float) -> bool:
        """Get a random boolean with given probability."""
        return MathUtils.random_bool(probability, self.rng)
    
    def random_choice(self, items: List):
        """Get a random choice from a list."""
        return self.rng.choice(items)
    
    def random_choices(self, items: List, k: int) -> List:
        """Get k random choices from a list (with replacement)."""
        return self.rng.choices(items, k=k)
    
    def shuffle(self, items: List) -> List:
        """Shuffle a list and return it."""
        shuffled = items.copy()
        self.rng.shuffle(shuffled)
        return shuffled
    
    def random_subset(self, items: List, size: int) -> List:
        """Get a random subset of given size without replacement."""
        if size >= len(items):
            return self.shuffle(items)
        return self.rng.sample(items, size)
    
    def weighted_choice(self, items: List, weights: List[float]):
        """Get a random choice with weighted probabilities."""
        return self.rng.choices(items, weights=weights, k=1)[0]
