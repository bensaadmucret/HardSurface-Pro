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
Math utilities for geometric calculations.
Provides functions for interpolation, distribution, and noise.
"""

import random
from typing import Tuple
from mathutils import Vector


class MathUtils:
    """Utility class for math operations."""
    
    @staticmethod
    def lerp(min_val: float, max_val: float, t: float) -> float:
        """Linear interpolation between min and max."""
        return min_val + (max_val - min_val) * t
    
    @staticmethod
    def random_range(min_val: float, max_val: float, rng: random.Random) -> float:
        """Get a random value between min and max using a specific RNG."""
        return rng.uniform(min_val, max_val)
    
    @staticmethod
    def random_int_range(min_val: int, max_val: int, rng: random.Random) -> int:
        """Get a random integer between min and max using a specific RNG."""
        return rng.randint(min_val, max_val)
    
    @staticmethod
    def clamp(value: float, min_val: float, max_val: float) -> float:
        """Clamp a value between min and max."""
        return max(min_val, min(value, max_val))
    
    @staticmethod
    def map_range(value: float, in_min: float, in_max: float, out_min: float, out_max: float) -> float:
        """Map a value from one range to another."""
        if in_max == in_min:
            return out_min
        t = (value - in_min) / (in_max - in_min)
        return out_min + t * (out_max - out_min)
    
    @staticmethod
    def random_bool(probability: float, rng: random.Random) -> bool:
        """Get a random boolean with given probability."""
        return rng.random() < probability
    
    @staticmethod
    def distance_point_to_plane(point: Vector, plane_point: Vector, plane_normal: Vector) -> float:
        """Calculate distance from a point to a plane."""
        return (point - plane_point).dot(plane_normal)
    
    @staticmethod
    def project_point_on_plane(point: Vector, plane_point: Vector, plane_normal: Vector) -> Vector:
        """Project a point onto a plane."""
        distance = MathUtils.distance_point_to_plane(point, plane_point, plane_normal)
        return point - plane_normal * distance
