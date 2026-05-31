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
Random Panels generator.
Orchestrates the generation of random panels on selected faces.
"""

import bmesh
import bpy
from typing import Optional, Tuple
from ..algorithms.randomization import Randomization
from ..algorithms.inset_ops import InsetOperations
from ...services.selection_service import SelectionService
from ...services.object_service import ObjectService
from ...utils.bmesh_utils import BMeshUtils
from ...utils.logging import Logger


class PanelsGenerator:
    """Generator for random panels on mesh faces."""
    
    def __init__(self, seed: int):
        """Initialize generator with a seed."""
        self.seed = seed
        self.rng = Randomization(seed)
        self.inset_ops = InsetOperations(self.rng)
    
    def generate(
        self,
        obj: bpy.types.Object,
        probability: float,
        inset_min: float,
        inset_max: float,
        depth_min: float,
        depth_max: float,
        safety_margin: float,
        use_copy: bool = False,
        use_materials: bool = False,
        bevel_amount: float = 0.0
    ) -> Tuple[bool, str]:
        """
        Generate random panels on selected faces.
        Returns (success, message).
        """
        # Validate selection
        is_valid, error = SelectionService.validate_face_selection(obj)
        if not is_valid:
            return False, error
        
        # Work on copy if requested
        if use_copy:
            obj = ObjectService.duplicate_object(obj)
            ObjectService.switch_to_edit_mode(obj)
        
        # Get bmesh
        bm = BMeshUtils.get_edit_bmesh(obj)
        if bm is None:
            return False, "Failed to get bmesh in Edit Mode"
        
        # Get selected faces
        selected_face_indices = SelectionService.get_selected_faces(obj)
        bm.faces.ensure_lookup_table()
        selected_faces = [bm.faces[i] for i in selected_face_indices if i < len(bm.faces)]
        
        if not selected_faces:
            return False, "No valid faces selected"
        
        Logger.info(f"Generating panels on {len(selected_faces)} faces with seed {self.seed}")
        
        # Apply inset with depth to each face
        affected_count = 0
        for face in selected_faces:
            result = self.inset_ops.apply_inset_with_depth(
                bm,
                face,
                inset_min,
                inset_max,
                depth_min,
                depth_max,
                probability,
                safety_margin,
                use_materials,
                bevel_amount
            )
            
            if result is not None:
                affected_count += 1
        
        # Update mesh
        bm.normal_update()
        BMeshUtils.apply_to_object(bm, obj)
        
        Logger.info(f"Generated {affected_count} panels")
        
        return True, f"Generated {affected_count} panels"
    
    def get_config_dict(self) -> dict:
        """Get current configuration as dictionary for presets."""
        return {
            'seed': self.seed,
            'type': 'random_panels'
        }
