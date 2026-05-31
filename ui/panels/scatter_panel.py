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
Random Scatter panel.
Sub-panel for Random Scatter operations.
"""

import bpy
from bpy.types import Panel


class VIEW3D_PT_hardsurface_scatter(Panel):
    """Random Scatter panel"""
    bl_label = "Random Scatter"
    bl_idname = "VIEW3D_PT_hardsurface_scatter"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'HardSurface'
    bl_parent_id = "VIEW3D_PT_hardsurface_main"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        """Draw the Random Scatter panel."""
        layout = self.layout
        wm = context.window_manager
        
        # Get properties
        if hasattr(wm, 'random_scatter_props'):
            props = wm.random_scatter_props
        else:
            return
        
        # Seed section
        box = layout.box()
        box.label(text="Seed", icon='TIME')
        row = box.row()
        row.prop(props, "seed")
        row.operator("hardsurface.randomize_seed", text="", icon='FILE_REFRESH')
        
        layout.separator()
        
        # Parameters
        box = layout.box()
        box.label(text="Parameters", icon='PROPERTIES')
        
        box.prop_search(props, "collection_name", bpy.data, "collections")
        box.prop(props, "density")
        box.prop(props, "rotation_min")
        box.prop(props, "rotation_max")
        box.prop(props, "scale_min")
        box.prop(props, "scale_max")
        box.prop(props, "align_to_normal")
        box.prop(props, "surface_offset")
        
        layout.separator()
        
        # Action button
        layout.operator("mesh.random_scatter", icon='GROUP_VERTEX')
