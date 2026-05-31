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
Inset operations for panel generation.
Provides algorithms for creating inset panels on faces.
"""

import bmesh
from typing import List, Optional
from ...utils.bmesh_utils import BMeshUtils
from ...utils.math_utils import MathUtils
from .randomization import Randomization


class InsetOperations:
    """Operations for creating inset panels."""
    
    def __init__(self, rng: Randomization):
        """Initialize with a randomization instance."""
        self.rng = rng
    
    def apply_random_inset(
        self,
        bm: bmesh.types.BMesh,
        face: bmesh.types.BMFace,
        inset_min: float,
        inset_max: float,
        probability: float = 1.0,
        safety_margin: float = 0.0
    ) -> Optional[bmesh.types.BMFace]:
        """
        Apply a random inset to a face with given probability.
        Returns the new inset face or None if not applied.
        """
        if not self.rng.random_bool(probability):
            return None
        
        inset_amount = self.rng.random_float(inset_min, inset_max)
        
        # Calculate maximum safe inset to prevent geometry collapsing/overlapping
        shortest_edge = min(edge.calc_length() for edge in face.edges) if face.edges else 0.0
        max_safe_inset = max(0.0001, (shortest_edge * 0.5) - safety_margin)
        
        # Clamp the inset amount to max_safe_inset
        inset_amount = min(inset_amount, max_safe_inset)
        
        return BMeshUtils.inset_face(bm, face, inset_amount)
    
    def apply_inset_with_depth(
        self,
        bm: bmesh.types.BMesh,
        face: bmesh.types.BMFace,
        inset_min: float,
        inset_max: float,
        depth_min: float,
        depth_max: float,
        probability: float = 1.0,
        safety_margin: float = 0.0,
        use_materials: bool = False,
        bevel_amount: float = 0.0
    ) -> Optional[bmesh.types.BMFace]:
        """
        Apply inset followed by extrusion with random depth.
        Supports automatic valley materials and panel edge beveling.
        Returns the final face or None if not applied.
        """
        # Track old faces to identify newly created valley faces during inset
        old_faces = set(bm.faces) if use_materials else None
        
        inset_face = self.apply_random_inset(
            bm, face, inset_min, inset_max, probability, safety_margin
        )
        
        if inset_face is None:
            return None
            
        # Assign valley materials to the inset border
        if use_materials and old_faces:
            new_faces = set(bm.faces) - old_faces
            for f in new_faces:
                if f != inset_face:
                    f.material_index = 1
        
        depth = self.rng.random_float(depth_min, depth_max)
        
        # Track old faces to identify extrusion side walls
        old_faces_ext = set(bm.faces) if use_materials else None
        
        extruded_face = BMeshUtils.extrude_face(bm, inset_face, depth)
        if extruded_face is None:
            return inset_face
            
        # Assign valley materials to extrusion side walls
        if use_materials and old_faces_ext:
            new_ext_faces = set(bm.faces) - old_faces_ext
            for f in new_ext_faces:
                if f != extruded_face:
                    f.material_index = 1
                    
        # Apply procedural beveling on panel cap edges
        if bevel_amount > 0.0 and len(extruded_face.edges) > 0:
            bmesh.ops.bevel(
                bm,
                geom=list(extruded_face.edges),
                offset=bevel_amount,
                offset_type='OFFSET',
                affect='EDGES'
            )
            
        return extruded_face
    
    def batch_apply_inset(
        self,
        bm: bmesh.types.BMesh,
        faces: List[bmesh.types.BMFace],
        inset_min: float,
        inset_max: float,
        probability: float,
        safety_margin: float = 0.0
    ) -> List[Optional[bmesh.types.BMFace]]:
        """
        Apply random inset to multiple faces.
        Returns list of new faces (None for faces not affected).
        """
        results = []
        for face in faces:
            result = self.apply_random_inset(
                bm, face, inset_min, inset_max, probability, safety_margin
            )
            results.append(result)
        return results
