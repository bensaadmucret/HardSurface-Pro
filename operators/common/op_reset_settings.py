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
Reset Settings operator.
Resets all operator properties to their default values.
"""

import bpy
from bpy.types import Operator
from ...utils.blender_utils import BlenderUtils


class OBJECT_OT_reset_settings(Operator):
    """Reset all settings to defaults"""
    bl_idname = "hardsurface.reset_settings"
    bl_label = "Reset Settings"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        """Reset all properties to default values."""
        wm = context.window_manager
        
        # Reset Random Panels props
        if hasattr(wm, 'random_panels_props'):
            props = wm.random_panels_props
            props.seed = 0
            props.probability = 0.5
            props.inset_min = 0.02
            props.inset_max = 0.1
            props.depth_min = -0.05
            props.depth_max = 0.05
            props.safety_margin = 0.01
            props.use_copy = False
        
        # Reset Random Extrude props
        if hasattr(wm, 'random_extrude_props'):
            props = wm.random_extrude_props
            props.seed = 0
            props.extrude_rate = 0.5
            props.height_min = 0.2
            props.height_max = 1.0
            props.taper_min = 0.0
            props.taper_max = 0.2
            props.max_faces = 100
            props.group_islands = False
        
        # Reset Random Scatter props
        if hasattr(wm, 'random_scatter_props'):
            props = wm.random_scatter_props
            props.seed = 0
            props.collection_name = ""
            props.density = 1.0
            props.rotation_min = 0.0
            props.rotation_max = 360.0
            props.scale_min = 0.5
            props.scale_max = 1.5
            props.align_to_normal = True
            props.surface_offset = 0.0
        
        # Reset Random Tubes props
        if hasattr(wm, 'random_tubes_props'):
            props = wm.random_tubes_props
            props.seed = 0
            props.radius = 0.1
            props.radius_variation = 0.5
            props.segments = 16
            props.smooth = True
        
        # Reset Random Loop Extrude props
        if hasattr(wm, 'random_loop_extrude_props'):
            props = wm.random_loop_extrude_props
            props.seed = 0
            props.iterations = 2
            props.probability = 0.7
            props.height_min = 0.05
            props.height_max = 0.3
            props.height_decay = 0.7
            props.inset_min = 0.02
            props.inset_max = 0.1
            props.taper = 0.0
            props.use_copy = False
        
        # Reset Panel Screws props
        if hasattr(wm, 'panel_screws_props'):
            props = wm.panel_screws_props
            props.seed = 0
            props.screw_size = 0.02
            props.screw_depth = 0.005
            props.probability = 0.8
            props.screw_type = 0
        
        # Reset Random Axis Extrude props
        if hasattr(wm, 'random_axis_extrude_props'):
            props = wm.random_axis_extrude_props
            props.seed = 0
            props.iterations = 2
            props.probability_x = 0.5
            props.probability_y = 0.5
            props.probability_z = 0.5
            props.length_min = 0.1
            props.length_max = 0.5
            props.scale_decay = 0.7
            props.use_copy = False
        
        # Reset Random Cells props
        if hasattr(wm, 'random_cells_props'):
            props = wm.random_cells_props
            props.seed = 0
            props.cell_type = 'PLANE'
            props.density = 0.3
            props.size_min = 0.05
            props.size_max = 0.2
            props.height_min = 0.1
            props.height_max = 0.5
            props.align_to_normal = True
            props.use_copy = False
        
        # Reset Random Cables props
        if hasattr(wm, 'random_cables_props'):
            props = wm.random_cables_props
            props.seed = 0
            props.cable_type = 'CATENARY'
            props.count = 3
            props.radius = 0.02
            props.slack = 0.3
            props.resolution = 12
            props.length_min = 1.0
            props.length_max = 3.0
        
        # Reset Flanges props
        if hasattr(wm, 'flanges_props'):
            props = wm.flanges_props
            props.seed = 0
            props.flange_size = 0.05
            props.flange_depth = 0.02
            props.spacing = 0.5
            props.probability = 0.8
            props.use_existing_curve = False
        
        # Force UI redraw so panels show updated values
        for area in context.screen.areas:
            if area.type == 'VIEW_3D':
                area.tag_redraw()
        
        BlenderUtils.report_info(self, "Settings reset to defaults")
        return {'FINISHED'}
