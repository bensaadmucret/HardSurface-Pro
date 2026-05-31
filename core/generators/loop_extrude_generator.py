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
Random Loop Extrude generator (Greeble Stacks).
Recursively insets and extrudes selected faces over multiple iterations.
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


class LoopExtrudeGenerator:
    """Generator for recursive loop extrusion (greeble stacks)."""
    
    def __init__(self, seed: int):
        self.seed = seed
        self.rng = Randomization(seed)
    
    def generate(
        self,
        obj: bpy.types.Object,
        iterations: int,
        probability: float,
        height_min: float,
        height_max: float,
        height_decay: float,
        inset_min: float,
        inset_max: float,
        taper: float,
        use_copy: bool = False
    ) -> Tuple[bool, str]:
        """
        Generate recursive greeble stacks on selected faces.
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
        
        Logger.info(f"Loop extruding {len(current_faces)} faces, {iterations} iterations")
        
        total_affected = 0
        for iteration in range(iterations):
            current_height_min = height_min * (height_decay ** iteration)
            current_height_max = height_max * (height_decay ** iteration)
            current_inset_min = inset_min * (height_decay ** iteration)
            current_inset_max = inset_max * (height_decay ** iteration)
            
            next_faces = []
            for face in current_faces:
                if not self.rng.random_bool(probability):
                    continue
                
                result = self._loop_step(
                    bm, face,
                    current_inset_min, current_inset_max,
                    current_height_min, current_height_max,
                    taper
                )
                
                if result is not None:
                    next_faces.append(result)
                    total_affected += 1
            
            current_faces = next_faces
            if not current_faces:
                break
        
        bm.normal_update()
        BMeshUtils.apply_to_object(bm, obj)
        
        return True, f"Generated greeble stacks on {total_affected} faces"
    
    def _loop_step(
        self,
        bm: bmesh.types.BMesh,
        face: bmesh.types.BMFace,
        inset_min: float,
        inset_max: float,
        height_min: float,
        height_max: float,
        taper: float
    ) -> bmesh.types.BMFace:
        """Perform one inset + extrude step on a face. Returns the new cap face."""
        inset_amount = self.rng.random_float(inset_min, inset_max)
        
        shortest_edge = min(edge.calc_length() for edge in face.edges) if face.edges else 0.0
        max_safe_inset = max(0.0001, shortest_edge * 0.5)
        inset_amount = min(inset_amount, max_safe_inset)
        
        geom = [face]
        result = bmesh.ops.inset_individual(
            bm,
            faces=geom,
            thickness=inset_amount,
            use_even_offset=False
        )
        
        inset_face = result['faces'][0] if result.get('faces') else None
        if inset_face is None:
            return None
        
        height = self.rng.random_float(height_min, height_max)
        
        extrude_result = bmesh.ops.extrude_face_region(bm, geom=[inset_face])
        if extrude_result.get('faces'):
            new_faces = extrude_result['faces']
            normal = inset_face.normal.copy()
            bmesh.ops.translate(bm, vec=normal * height, verts=extrude_result['verts'])
            
            if taper > 0 and extrude_result.get('verts'):
                center = inset_face.calc_center_median()
                for v in extrude_result['verts']:
                    direction = (v.co - center).normalized()
                    v.co -= direction * taper * inset_amount
            
            return new_faces[0] if new_faces else None
        
        return inset_face
