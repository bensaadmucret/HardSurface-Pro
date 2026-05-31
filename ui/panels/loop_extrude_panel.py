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
Loop Extrude (Greeble Stacks) panel for the N-Panel sidebar.
"""

import bpy
from bpy.types import Panel


class VIEW3D_PT_hardsurface_loop_extrude(Panel):
    """Loop Extrude settings panel"""
    bl_label = "Loop Extrude"
    bl_idname = "VIEW3D_PT_hardsurface_loop_extrude"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "HardSurface"
    bl_parent_id = "VIEW3D_PT_hardsurface_main"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        wm = context.window_manager
        
        if hasattr(wm, 'random_loop_extrude_props'):
            props = wm.random_loop_extrude_props
            
            col = layout.column(align=True)
            col.prop(props, "seed")
            col.prop(props, "iterations")
            col.prop(props, "probability")
            
            col.separator()
            col.prop(props, "height_min")
            col.prop(props, "height_max")
            col.prop(props, "height_decay")
            
            col.separator()
            col.prop(props, "inset_min")
            col.prop(props, "inset_max")
            col.prop(props, "taper")
            
            col.separator()
            col.prop(props, "use_copy")
        
        layout.separator()
        layout.operator("mesh.random_loop_extrude", icon='MOD_ARRAY')
