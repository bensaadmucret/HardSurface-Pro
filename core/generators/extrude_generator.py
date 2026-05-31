# HardSurface Pro - Procedural Hard-Surface Generation Addon for Blender
# Copyright (C) 2024 HardSurface Pro Contributors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

"""
Random Extrude generator.
Orchestrates the generation of random extrusions on selected faces.
"""

import bmesh
import bpy
from typing import Optional, Tuple
from ..algorithms.randomization import Randomization
from ..algorithms.extrude_ops import ExtrusionOperations
from ...services.selection_service import SelectionService
from ...services.object_service import ObjectService
from ...utils.bmesh_utils import BMeshUtils
from ...utils.logging import Logger


class ExtrudeGenerator:
    """Generator for random extrusions on mesh faces."""
    
    def __init__(self, seed: int):
        """Initialize generator with a seed."""
        self.seed = seed
        self.rng = Randomization(seed)
        self.extrude_ops = ExtrusionOperations(self.rng)
    
    def generate(
        self,
        obj: bpy.types.Object,
        extrude_rate: float,
        height_min: float,
        height_max: float,
        taper_min: float,
        taper_max: float,
        max_faces: int,
        group_islands: bool = False
    ) -> Tuple[bool, str]:
        """
        Generate random extrusions on selected faces.
        Returns (success, message).
        """
        # Validate selection
        is_valid, error = SelectionService.validate_face_selection(obj)
        if not is_valid:
            return False, error
        
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
        
        Logger.info(f"Generating extrusions on {len(selected_faces)} faces with seed {self.seed}")
        
        # Apply extrusions
        affected_count = 0
        
        if group_islands:
            # Group the selected faces into contiguous islands
            islands = self.extrude_ops.find_face_islands(selected_faces)
            
            # Shuffle islands for seed-based randomization
            shuffled_islands = self.rng.shuffle(islands)
            
            for island in shuffled_islands:
                # Stop if adding this island would exceed max_faces
                if affected_count + len(island) > max_faces:
                    continue
                
                # Roll extrusion rate
                if self.rng.random_bool(extrude_rate):
                    result = self.extrude_ops.apply_group_extrude_with_taper(
                        bm,
                        island,
                        height_min,
                        height_max,
                        taper_min,
                        taper_max
                    )
                    if result:
                        affected_count += len(island)
        else:
            # Shuffle faces for seed-based randomization
            shuffled_faces = self.rng.shuffle(selected_faces)
            
            for face in shuffled_faces:
                # Stop if we hit the limit
                if affected_count >= max_faces:
                    break
                
                result = self.extrude_ops.apply_extrude_with_taper(
                    bm,
                    face,
                    height_min,
                    height_max,
                    taper_min,
                    taper_max,
                    extrude_rate
                )
                
                if result is not None:
                    affected_count += 1
        
        # Update mesh
        bm.normal_update()
        BMeshUtils.apply_to_object(bm, obj)
        
        Logger.info(f"Generated {affected_count} extrusions")
        
        return True, f"Generated {affected_count} extrusions"
    
    def get_config_dict(self) -> dict:
        """Get current configuration as dictionary for presets."""
        return {
            'seed': self.seed,
            'type': 'random_extrude'
        }
