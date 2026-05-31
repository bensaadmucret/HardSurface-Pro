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
Randomize Seed operator.
Generates a new random seed for the current operator context.
"""

import bpy
from bpy.types import Operator
from ...services.seed_service import SeedService
from ...utils.blender_utils import BlenderUtils


class OBJECT_OT_randomize_seed(Operator):
    """Generate a new random seed"""
    bl_idname = "hardsurface.randomize_seed"
    bl_label = "Randomize Seed"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        """Generate and set a new random seed."""
        new_seed = SeedService.generate()
        
        # Update all property groups
        wm = context.window_manager
        if hasattr(wm, 'random_panels_props'):
            wm.random_panels_props.seed = new_seed
        if hasattr(wm, 'random_extrude_props'):
            wm.random_extrude_props.seed = new_seed
        if hasattr(wm, 'random_scatter_props'):
            wm.random_scatter_props.seed = new_seed
        if hasattr(wm, 'random_tubes_props'):
            wm.random_tubes_props.seed = new_seed
        if hasattr(wm, 'random_loop_extrude_props'):
            wm.random_loop_extrude_props.seed = new_seed
        if hasattr(wm, 'panel_screws_props'):
            wm.panel_screws_props.seed = new_seed
        if hasattr(wm, 'random_axis_extrude_props'):
            wm.random_axis_extrude_props.seed = new_seed
        if hasattr(wm, 'random_cells_props'):
            wm.random_cells_props.seed = new_seed
        if hasattr(wm, 'random_cables_props'):
            wm.random_cables_props.seed = new_seed
        if hasattr(wm, 'flanges_props'):
            wm.flanges_props.seed = new_seed
        
        BlenderUtils.report_info(self, f"New seed: {new_seed}")
        return {'FINISHED'}
