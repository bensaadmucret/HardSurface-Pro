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
Random Tubes panel.
Sub-panel for Random Tubes operations.
"""

import bpy
from bpy.types import Panel


class VIEW3D_PT_hardsurface_tubes(Panel):
    """Random Tubes panel"""
    bl_label = "Random Tubes"
    bl_idname = "VIEW3D_PT_hardsurface_tubes"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'HardSurface'
    bl_parent_id = "VIEW3D_PT_hardsurface_main"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        """Draw the Random Tubes panel."""
        layout = self.layout
        wm = context.window_manager
        
        # Get properties
        if hasattr(wm, 'random_tubes_props'):
            props = wm.random_tubes_props
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
        
        box.prop(props, "radius")
        box.prop(props, "radius_variation")
        box.prop(props, "segments")
        box.prop(props, "smooth")
        
        layout.separator()
        
        # Action button
        layout.operator("mesh.random_tubes", icon='CURVE_BEZCURVE')
