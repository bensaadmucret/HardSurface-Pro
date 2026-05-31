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
Seed service for managing random seeds.
Provides generation, locking, and mutation of seeds for reproducible results.
"""

import random
from typing import Optional


class SeedService:
    """Service for managing random seeds."""
    
    @staticmethod
    def generate() -> int:
        """Generate a new random seed."""
        return random.randint(0, 2**31 - 1)
    
    @staticmethod
    def mutate(seed: int, offset: int = 1) -> int:
        """Mutate a seed by adding an offset."""
        return (seed + offset) % (2**31)
    
    @staticmethod
    def validate(seed: int) -> bool:
        """Validate that a seed is within acceptable range."""
        return 0 <= seed < 2**31
    
    @staticmethod
    def create_random_generator(seed: int) -> random.Random:
        """Create a random.Random instance with a specific seed."""
        return random.Random(seed)
