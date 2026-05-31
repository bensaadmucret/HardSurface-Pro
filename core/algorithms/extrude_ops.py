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
Extrusion operations for random extrusion.
Provides algorithms for creating random extrusions on faces.
"""

import bmesh
from typing import List, Optional
from ...utils.bmesh_utils import BMeshUtils
from .randomization import Randomization


class ExtrusionOperations:
    """Operations for creating random extrusions."""
    
    def __init__(self, rng: Randomization):
        """Initialize with a randomization instance."""
        self.rng = rng
    
    def apply_random_extrude(
        self,
        bm: bmesh.types.BMesh,
        face: bmesh.types.BMFace,
        height_min: float,
        height_max: float,
        probability: float = 1.0
    ) -> Optional[bmesh.types.BMFace]:
        """
        Apply a random extrusion to a face with given probability.
        Returns the new extruded face or None if not applied.
        """
        if not self.rng.random_bool(probability):
            return None
        
        height = self.rng.random_float(height_min, height_max)
        return BMeshUtils.extrude_face(bm, face, height)
    
    def apply_extrude_with_taper(
        self,
        bm: bmesh.types.BMesh,
        face: bmesh.types.BMFace,
        height_min: float,
        height_max: float,
        taper_min: float,
        taper_max: float,
        probability: float = 1.0
    ) -> Optional[bmesh.types.BMFace]:
        """
        Apply extrusion with taper effect.
        Note: Full taper implementation requires additional geometry manipulation.
        This is a simplified version for MVP.
        """
        extruded_face = self.apply_random_extrude(
            bm, face, height_min, height_max, probability
        )
        
        if extruded_face is None:
            return None
        
        # Simplified taper: scale the top face
        taper = self.rng.random_float(taper_min, taper_max)
        if taper > 0:
            scale_factor = 1.0 - taper
            center = BMeshUtils.get_face_center(extruded_face)
            normal = BMeshUtils.get_face_normal(extruded_face)
            
            # Scale vertices along the face plane
            for vert in extruded_face.verts:
                vec = vert.co - center
                # Project onto face plane
                projected = vec - vec.dot(normal) * normal
                vert.co = center + projected * scale_factor + vec.dot(normal) * normal
        
        return extruded_face
    
    def batch_apply_extrude(
        self,
        bm: bmesh.types.BMesh,
        faces: List[bmesh.types.BMFace],
        height_min: float,
        height_max: float,
        extrude_rate: float,
        max_faces: int
    ) -> List[Optional[bmesh.types.BMFace]]:
        """
        Apply random extrusion to multiple faces with rate limiting.
        Returns list of new faces (None for faces not affected).
        """
        # Limit number of faces to affect
        faces_to_process = self.rng.random_subset(faces, min(max_faces, len(faces)))
        
        results = []
        for face in faces:
            if face in faces_to_process:
                result = self.apply_random_extrude(
                    bm, face, height_min, height_max, extrude_rate
                )
                results.append(result)
            else:
                results.append(None)
        return results
    
    def find_face_islands(
        self,
        faces: List[bmesh.types.BMFace]
    ) -> List[List[bmesh.types.BMFace]]:
        """
        Group a list of faces into contiguous islands.
        Faces are contiguous if they share an edge.
        """
        face_set = set(faces)
        visited = set()
        islands = []
        
        for face in faces:
            if face in visited:
                continue
            
            # BFS connectivity check
            island = []
            queue = [face]
            visited.add(face)
            
            while queue:
                curr = queue.pop(0)
                island.append(curr)
                
                for edge in curr.edges:
                    for other_face in edge.link_faces:
                        if other_face in face_set and other_face not in visited:
                            visited.add(other_face)
                            queue.append(other_face)
            islands.append(island)
            
        return islands
        
    def apply_group_extrude_with_taper(
        self,
        bm: bmesh.types.BMesh,
        faces: List[bmesh.types.BMFace],
        height_min: float,
        height_max: float,
        taper_min: float,
        taper_max: float
    ) -> Optional[List[bmesh.types.BMFace]]:
        """
        Extrude a region/island of faces as a single block with random height and taper.
        """
        if not faces:
            return None
        
        from mathutils import Vector
        
        # Calculate average normal of original faces before extrusion
        avg_normal = Vector((0.0, 0.0, 0.0))
        for face in faces:
            avg_normal += face.normal
        if avg_normal.length > 0.001:
            avg_normal.normalize()
        else:
            avg_normal = Vector((0.0, 0.0, 1.0))
        
        # Perform extrusion
        result = bmesh.ops.extrude_face_region(bm, geom=faces)
        if not result or not result.get('verts'):
            return None
        
        # Determine random height
        height = self.rng.random_float(height_min, height_max)
        
        # Translate the new cap vertices along the average normal
        bmesh.ops.translate(bm, vec=avg_normal * height, verts=result['verts'])
        
        # Apply taper to the new cap vertices relative to their global centroid
        taper = self.rng.random_float(taper_min, taper_max)
        if taper > 0.0 and len(result['verts']) > 0:
            scale_factor = 1.0 - taper
            
            # Calculate centroid of the new cap vertices
            centroid = Vector((0.0, 0.0, 0.0))
            for v in result['verts']:
                centroid += v.co
            centroid /= len(result['verts'])
            
            # Scale each vertex relative to centroid along the plane perp to avg_normal
            for v in result['verts']:
                vec = v.co - centroid
                projected = vec - vec.dot(avg_normal) * avg_normal
                v.co = centroid + projected * scale_factor + vec.dot(avg_normal) * avg_normal
        
        return result.get('faces')
