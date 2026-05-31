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
Panel Screws panel for the N-Panel sidebar.
"""

import bpy
from bpy.types import Panel


class VIEW3D_PT_hardsurface_screws(Panel):
    """Panel Screws settings panel"""
    bl_label = "Panel Screws"
    bl_idname = "VIEW3D_PT_hardsurface_screws"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "HardSurface"
    bl_parent_id = "VIEW3D_PT_hardsurface_main"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        wm = context.window_manager
        
        if hasattr(wm, 'panel_screws_props'):
            props = wm.panel_screws_props
            
            col = layout.column(align=True)
            col.prop(props, "seed")
            col.prop(props, "screw_size")
            col.prop(props, "screw_depth")
            col.prop(props, "probability")
            col.prop(props, "screw_type")
        
        layout.separator()
        layout.operator("mesh.panel_screws", icon='DECORATE')
