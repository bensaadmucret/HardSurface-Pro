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
Random Tubes generator.
Orchestrates the generation of tubes from edges or points.
"""

import bpy
import bmesh
from mathutils import Vector
from typing import Tuple, List
from ..algorithms.randomization import Randomization
from ...services.selection_service import SelectionService
from ...services.object_service import ObjectService
from ...utils.bmesh_utils import BMeshUtils
from ...utils.logging import Logger


class TubesGenerator:
    """Generator for creating tubes from edges."""
    
    def __init__(self, seed: int):
        """Initialize generator with a seed."""
        self.seed = seed
        self.rng = Randomization(seed)
    
    def generate(
        self,
        obj: bpy.types.Object,
        radius: float,
        radius_variation: float,
        segments: int,
        smooth: bool
    ) -> Tuple[bool, str]:
        """
        Generate tubes from selected edges.
        Returns (success, message).
        """
        # Validate selection
        is_valid, error = SelectionService.validate_mesh_object(obj)
        if not is_valid:
            return False, error
        
        if obj.mode != 'EDIT':
            return False, "Object must be in Edit Mode with edges selected"
        
        # Get bmesh
        bm = BMeshUtils.get_edit_bmesh(obj)
        if bm is None:
            return False, "Failed to get bmesh in Edit Mode"
        
        # Get selected edges
        selected_edge_indices = SelectionService.get_selected_edges(obj)
        bm.edges.ensure_lookup_table()
        selected_edges = [bm.edges[i] for i in selected_edge_indices if i < len(bm.edges)]
        
        if not selected_edges:
            return False, "No edges selected"
        
        Logger.info(f"Generating tubes from {len(selected_edges)} edges with seed {self.seed}")
        
        # Create tubes from edges
        created_tubes = []
        for edge in selected_edges:
            tube = self._create_tube_from_edge(
                edge,
                radius,
                radius_variation,
                segments
            )
            if tube:
                created_tubes.append(tube)
        
        # Apply smooth shading by converting curves to meshes
        if smooth and created_tubes:
            bpy.ops.object.mode_set(mode='OBJECT')
            for tube in created_tubes:
                for o in bpy.context.selected_objects:
                    o.select_set(False)
                tube.select_set(True)
                bpy.context.view_layer.objects.active = tube
                bpy.ops.object.convert(target='MESH')
                if tube.data and hasattr(tube.data, 'polygons'):
                    for poly in tube.data.polygons:
                        poly.use_smooth = True
            # Restore context
            for o in bpy.context.selected_objects:
                o.select_set(False)
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.mode_set(mode='EDIT')
        
        Logger.info(f"Created {len(created_tubes)} tubes")
        return True, f"Created {len(created_tubes)} tubes"
    
    def _create_tube_from_edge(
        self,
        edge: bmesh.types.BMEdge,
        base_radius: float,
        radius_variation: float,
        segments: int
    ) -> bpy.types.Object:
        """Create a tube from a single edge."""
        # Get edge vertices
        v1, v2 = edge.verts
        start = v1.co.copy()
        end = v2.co.copy()
        
        # Calculate edge length and direction
        edge_vector = end - start
        length = edge_vector.length
        
        if length < 0.001:
            return None
        
        # Calculate radius with variation
        radius = base_radius * (1.0 + self.rng.random_float(-radius_variation, radius_variation))
        radius = max(0.001, radius)
        
        # Create curve
        curve_data = bpy.data.curves.new(name="TubeCurve", type='CURVE')
        curve_data.dimensions = '3D'
        curve_data.bevel_depth = radius
        curve_data.bevel_resolution = segments // 4
        
        # Add spline
        spline = curve_data.splines.new('POLY')
        spline.points.add(1)
        
        # Set points
        spline.points[0].co = (start.x, start.y, start.z, 1)
        spline.points[1].co = (end.x, end.y, end.z, 1)
        
        # Create object
        tube_obj = bpy.data.objects.new("Tube", curve_data)
        bpy.context.collection.objects.link(tube_obj)
        
        return tube_obj
    
    def get_config_dict(self) -> dict:
        """Get current configuration as dictionary for presets."""
        return {
            'seed': self.seed,
            'type': 'random_tubes'
        }
