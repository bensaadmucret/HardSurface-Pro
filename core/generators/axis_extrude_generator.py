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
Random Axis Extrude generator.
Creates recursive branching extrusions in the XYZ axis.
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


class AxisExtrudeGenerator:
    """Generator for recursive axis-aligned branching extrusions."""
    
    def __init__(self, seed: int):
        self.seed = seed
        self.rng = Randomization(seed)
    
    def generate(
        self,
        obj: bpy.types.Object,
        iterations: int,
        prob_x: float,
        prob_y: float,
        prob_z: float,
        length_min: float,
        length_max: float,
        scale_decay: float,
        use_copy: bool = False
    ) -> Tuple[bool, str]:
        """
        Generate recursive axis-aligned extrusions on selected faces.
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
        current_faces = [bm.faces[i] for i in selected_face_indices if i < len(bm.faces)]
        
        if not current_faces:
            return False, "No valid faces selected"
        
        Logger.info(f"Axis extruding {len(current_faces)} faces, {iterations} iterations")
        
        total_branches = 0
        for iteration in range(iterations):
            next_faces = []
            for face in current_faces:
                branches = self._create_branches(
                    bm, face, prob_x, prob_y, prob_z,
                    length_min, length_max, scale_decay, iteration
                )
                next_faces.extend(branches)
                total_branches += len(branches)
            
            current_faces = next_faces
            if not current_faces:
                break
        
        bm.normal_update()
        BMeshUtils.apply_to_object(bm, obj)
        
        return True, f"Created {total_branches} axis branches"
    
    def _create_branches(
        self,
        bm: bmesh.types.BMesh,
        face: bmesh.types.BMFace,
        prob_x: float,
        prob_y: float,
        prob_z: float,
        length_min: float,
        length_max: float,
        scale_decay: float,
        iteration: int
    ) -> List[bmesh.types.BMFace]:
        """Create branches along X, Y, Z axes from a face."""
        branches = []
        axes = [
            (Vector((1, 0, 0)), prob_x),
            (Vector((0, 1, 0)), prob_y),
            (Vector((0, 0, 1)), prob_z),
        ]
        
        for axis, prob in axes:
            if not self.rng.random_bool(prob):
                continue
            
            length = self.rng.random_float(length_min, length_max) * (scale_decay ** iteration)
            
            result = bmesh.ops.extrude_face_region(bm, geom=[face])
            if result.get('faces'):
                new_face = result['faces'][0]
                direction = axis * length
                bmesh.ops.translate(bm, vec=direction, verts=result['verts'])
                branches.append(new_face)
        
        return branches
