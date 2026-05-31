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
Axis Extrude panel for the N-Panel sidebar.
"""

import bpy
from bpy.types import Panel


class VIEW3D_PT_hardsurface_axis_extrude(Panel):
    """Axis Extrude panel"""
    bl_label = "Axis Extrude"
    bl_idname = "VIEW3D_PT_hardsurface_axis_extrude"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "HardSurface"
    bl_parent_id = "VIEW3D_PT_hardsurface_main"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        wm = context.window_manager
        
        if not hasattr(wm, 'random_axis_extrude_props'):
            return
        props = wm.random_axis_extrude_props
        
        # Seed
        box = layout.box()
        row = box.row(align=True)
        row.prop(props, "seed", text="Seed")
        row.operator("hardsurface.randomize_seed", text="", icon='FILE_REFRESH')
        
        # Iterations
        box = layout.box()
        box.label(text="Branching", icon='MOD_ARRAY')
        split = box.split(factor=0.4)
        split.label(text="Iterations:")
        split.prop(props, "iterations", text="")
        
        # Axis Probabilities
        box = layout.box()
        box.label(text="Axis Probabilities", icon='ORIENTATION_GLOBAL')
        split = box.split(factor=0.4)
        split.label(text="X:")
        split.prop(props, "probability_x", text="")
        split = box.split(factor=0.4)
        split.label(text="Y:")
        split.prop(props, "probability_y", text="")
        split = box.split(factor=0.4)
        split.label(text="Z:")
        split.prop(props, "probability_z", text="")
        
        # Length
        box = layout.box()
        box.label(text="Length", icon='ARROW_LEFTRIGHT')
        split = box.split(factor=0.4)
        split.label(text="Length:")
        sub = split.row(align=True)
        sub.prop(props, "length_min", text="Min")
        sub.prop(props, "length_max", text="Max")
        
        split = box.split(factor=0.4)
        split.label(text="Decay:")
        split.prop(props, "scale_decay", text="")
        
        # Options
        box = layout.box()
        box.label(text="Options", icon='PREFERENCES')
        split = box.split(factor=0.4)
        split.label(text="Mode:")
        split.prop(props, "use_copy", text="Use Copy")
        
        layout.separator()
        
        # Action
        row = layout.row()
        row.scale_y = 1.5
        row.operator("mesh.random_axis_extrude", text="Generate Axis Branches", icon='MOD_SOLIDIFY')
