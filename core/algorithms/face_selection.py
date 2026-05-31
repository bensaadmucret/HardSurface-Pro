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
Face selection algorithms.
Provides utilities for selecting and filtering faces.
"""

import bmesh
from typing import List, Set
from .randomization import Randomization


class FaceSelection:
    """Operations for face selection and filtering."""
    
    def __init__(self, rng: Randomization):
        """Initialize with a randomization instance."""
        self.rng = rng
    
    def get_face_islands(self, bm: bmesh.types.BMesh) -> List[Set[int]]:
        """
        Group faces into connected islands.
        Returns list of sets, each containing face indices of an island.
        """
        visited = set()
        islands = []
        
        for face in bm.faces:
            if face.index in visited:
                continue
            
            # Start new island
            island = set()
            stack = [face]
            
            while stack:
                current = stack.pop()
                if current.index in visited:
                    continue
                
                visited.add(current.index)
                island.add(current.index)
                
                # Add adjacent faces
                for edge in current.edges:
                    for other_face in edge.link_faces:
                        if other_face.index not in visited:
                            stack.append(other_face)
            
            if island:
                islands.append(island)
        
        return islands
    
    def filter_by_area(
        self,
        faces: List[bmesh.types.BMFace],
        min_area: float = 0.0,
        max_area: float = float('inf')
    ) -> List[bmesh.types.BMFace]:
        """Filter faces by area."""
        return [
            face for face in faces
            if min_area <= face.calc_area() <= max_area
        ]
    
    def filter_by_normal(
        self,
        faces: List[bmesh.types.BMFace],
        reference_normal,
        angle_threshold: float = 30.0
    ) -> List[bmesh.types.BMFace]:
        """Filter faces by normal direction within angle threshold."""
        import math
        cos_threshold = math.cos(math.radians(angle_threshold))
        
        return [
            face for face in faces
            if face.normal.dot(reference_normal) >= cos_threshold
        ]
    
    def select_random_subset(
        self,
        faces: List[bmesh.types.BMFace],
        count: int
    ) -> List[bmesh.types.BMFace]:
        """Select a random subset of faces."""
        return self.rng.random_subset(faces, count)
