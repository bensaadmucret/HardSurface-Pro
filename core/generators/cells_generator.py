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
Random Cells generator.
Creates faces that act as emission planes or extruded antennae/boxes.
"""

import bmesh
import bpy
from typing import Tuple, List
from mathutils import Vector
from ..algorithms.randomization import Randomization
from ...services.selection_service import SelectionService
from ...services.object_service import ObjectService
from ...utils.bmesh_utils import BMeshUtils
from ...utils.logging import Logger


class CellsGenerator:
    """Generator for emission planes and antenna-like structures."""
    
    def __init__(self, seed: int):
        self.seed = seed
        self.rng = Randomization(seed)
    
    def generate(
        self,
        obj: bpy.types.Object,
        cell_type: str,
        density: float,
        size_min: float,
        size_max: float,
        height_min: float,
        height_max: float,
        align_to_normal: bool,
        use_copy: bool = False
    ) -> Tuple[bool, str]:
        """
        Generate cells on selected faces.
        Returns (success, message).
        """
        is_valid, error = SelectionService.validate_face_selection(obj)
        if not is_valid:
            return False, error
        
        if use_copy:
            obj = ObjectService.duplicate_object(obj)
            ObjectService.switch_to_edit_mode(obj)
        
        bm = BMeshUtils.get_edit_bmesh(obj)
        if bm is None:
            return False, "Failed to get bmesh in Edit Mode"
        
        selected_face_indices = SelectionService.get_selected_faces(obj)
        bm.faces.ensure_lookup_table()
        selected_faces = [bm.faces[i] for i in selected_face_indices if i < len(bm.faces)]
        
        if not selected_faces:
            return False, "No valid faces selected"
        
        Logger.info(f"Generating {cell_type} cells on {len(selected_faces)} faces")
        
        cells_created = 0
        for face in selected_faces:
            if not self.rng.random_bool(density):
                continue
            
            if cell_type == 'PLANE':
                self._create_plane_cell(bm, face, size_min, size_max, align_to_normal)
            elif cell_type == 'ANTENNA':
                self._create_antenna_cell(bm, face, size_min, size_max, height_min, height_max, align_to_normal)
            elif cell_type == 'BOX':
                self._create_box_cell(bm, face, size_min, size_max, height_min, height_max, align_to_normal)
            
            cells_created += 1
        
        bm.normal_update()
        BMeshUtils.apply_to_object(bm, obj)
        
        return True, f"Created {cells_created} {cell_type} cells"
    
    def _create_plane_cell(
        self,
        bm: bmesh.types.BMesh,
        face: bmesh.types.BMFace,
        size_min: float,
        size_max: float,
        align_to_normal: bool
    ):
        """Create a flat emission plane on the face."""
        size = self.rng.random_float(size_min, size_max)
        center = face.calc_center_median()
        normal = face.normal.copy() if align_to_normal else Vector((0, 0, 1))
        
        verts = []
        for dx, dy in [(-1, -1), (1, -1), (1, 1), (-1, 1)]:
            v = bm.verts.new(center + normal * 0.001 + Vector((dx * size, dy * size, 0)))
            verts.append(v)
        
        bm.faces.new(verts)
    
    def _create_antenna_cell(
        self,
        bm: bmesh.types.BMesh,
        face: bmesh.types.BMFace,
        size_min: float,
        size_max: float,
        height_min: float,
        height_max: float,
        align_to_normal: bool
    ):
        """Create a thin antenna extrusion."""
        center = face.calc_center_median()
        normal = face.normal.copy() if align_to_normal else Vector((0, 0, 1))
        height = self.rng.random_float(height_min, height_max)
        
        v1 = bm.verts.new(center + normal * 0.001)
        v2 = bm.verts.new(center + normal * (0.001 + height))
        bm.edges.new((v1, v2))
    
    def _create_box_cell(
        self,
        bm: bmesh.types.BMesh,
        face: bmesh.types.BMFace,
        size_min: float,
        size_max: float,
        height_min: float,
        height_max: float,
        align_to_normal: bool
    ):
        """Create a small box protrusion."""
        size = self.rng.random_float(size_min, size_max)
        height = self.rng.random_float(height_min, height_max)
        center = face.calc_center_median()
        normal = face.normal.copy() if align_to_normal else Vector((0, 0, 1))
        
        base = center + normal * 0.001
        top = base + normal * height
        
        # Create 4 base vertices
        base_verts = []
        for dx, dy in [(-1, -1), (1, -1), (1, 1), (-1, 1)]:
            v = bm.verts.new(base + Vector((dx * size, dy * size, 0)))
            base_verts.append(v)
        
        # Create 4 top vertices
        top_verts = []
        for dx, dy in [(-1, -1), (1, -1), (1, 1), (-1, 1)]:
            v = bm.verts.new(top + Vector((dx * size, dy * size, 0)))
            top_verts.append(v)
        
        # Create 6 faces (box)
        bm.faces.new(base_verts)  # bottom
        bm.faces.new(top_verts[::-1])  # top (reversed for correct normal)
        # sides
        for i in range(4):
            j = (i + 1) % 4
            bm.faces.new((base_verts[i], base_verts[j], top_verts[j], top_verts[i]))
