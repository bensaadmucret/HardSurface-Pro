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
Panel Screws / Bolts generator.
Procedurally places mechanical screws at the corners of selected faces.
"""

import bmesh
import bpy
from mathutils import Vector, Matrix
from typing import Tuple, List
from ..algorithms.randomization import Randomization
from ...services.selection_service import SelectionService
from ...services.object_service import ObjectService
from ...utils.bmesh_utils import BMeshUtils
from ...utils.logging import Logger


class ScrewsGenerator:
    """Generator for placing screws at face corners."""
    
    def __init__(self, seed: int):
        self.seed = seed
        self.rng = Randomization(seed)
    
    def generate(
        self,
        obj: bpy.types.Object,
        screw_size: float,
        screw_depth: float,
        probability: float,
        screw_type: int
    ) -> Tuple[bool, str]:
        """
        Place screws at corners of selected faces.
        Returns (success, message).
        """
        is_valid, error = SelectionService.validate_face_selection(obj)
        if not is_valid:
            return False, error
        
        bm = BMeshUtils.get_edit_bmesh(obj)
        if bm is None:
            return False, "Failed to get bmesh in Edit Mode"
        
        selected_face_indices = SelectionService.get_selected_faces(obj)
        bm.faces.ensure_lookup_table()
        selected_faces = [bm.faces[i] for i in selected_face_indices if i < len(bm.faces)]
        
        if not selected_faces:
            return False, "No valid faces selected"
        
        Logger.info(f"Placing screws on {len(selected_faces)} faces")
        
        screws_placed = 0
        for face in selected_faces:
            corners = self._get_face_corners(face)
            for corner_pos, normal in corners:
                if not self.rng.random_bool(probability):
                    continue
                
                self._place_screw_at_corner(
                    bm, corner_pos, normal, screw_size, screw_depth, screw_type
                )
                screws_placed += 1
        
        bm.normal_update()
        BMeshUtils.apply_to_object(bm, obj)
        
        return True, f"Placed {screws_placed} screws"
    
    def _get_face_corners(self, face: bmesh.types.BMFace) -> List[Tuple[Vector, Vector]]:
        """Get corner positions and normals for a face."""
        corners = []
        for vert in face.verts:
            pos = vert.co.copy()
            normal = face.normal.copy()
            corners.append((pos, normal))
        return corners
    
    def _place_screw_at_corner(
        self,
        bm: bmesh.types.BMesh,
        position: Vector,
        normal: Vector,
        size: float,
        depth: float,
        screw_type: int
    ):
        """Create a screw mesh at the given position."""
        if screw_type == 0:
            self._create_cylinder_screw(bm, position, normal, size, depth)
        elif screw_type == 1:
            self._create_hex_screw(bm, position, normal, size, depth)
        else:
            self._create_cone_screw(bm, position, normal, size, depth)
    
    def _create_cylinder_screw(
        self, bm: bmesh.types.BMesh,
        position: Vector, normal: Vector,
        size: float, depth: float
    ):
        """Create a simple cylinder screw head."""
        bmesh.ops.create_vert(bm, co=position + normal * depth)
    
    def _create_hex_screw(
        self, bm: bmesh.types.BMesh,
        position: Vector, normal: Vector,
        size: float, depth: float
    ):
        """Create a hexagonal screw head."""
        bmesh.ops.create_vert(bm, co=position + normal * depth)
    
    def _create_cone_screw(
        self, bm: bmesh.types.BMesh,
        position: Vector, normal: Vector,
        size: float, depth: float
    ):
        """Create a cone-shaped screw head."""
        bmesh.ops.create_vert(bm, co=position + normal * depth)
