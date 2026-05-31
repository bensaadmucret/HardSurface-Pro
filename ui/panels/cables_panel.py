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
Random Cables panel for the N-Panel sidebar.
"""

import bpy
from bpy.types import Panel


class VIEW3D_PT_hardsurface_cables(Panel):
    """Random Cables panel"""
    bl_label = "Random Cables"
    bl_idname = "VIEW3D_PT_hardsurface_cables"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "HardSurface"
    bl_parent_id = "VIEW3D_PT_hardsurface_main"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        wm = context.window_manager
        
        if not hasattr(wm, 'random_cables_props'):
            return
        props = wm.random_cables_props
        
        # Seed
        box = layout.box()
        row = box.row(align=True)
        row.prop(props, "seed", text="Seed")
        row.operator("hardsurface.randomize_seed", text="", icon='FILE_REFRESH')
        
        # Cable Type
        box = layout.box()
        box.label(text="Cable Type", icon='CURVE_DATA')
        row = box.row(align=True)
        row.prop(props, "cable_type", expand=True)
        
        # Count
        box = layout.box()
        box.label(text="Distribution", icon='PARTICLES')
        split = box.split(factor=0.4)
        split.label(text="Count:")
        split.prop(props, "count", text="")
        
        # Radius
        split = box.split(factor=0.4)
        split.label(text="Radius:")
        split.prop(props, "radius", text="")
        
        # Slack
        split = box.split(factor=0.4)
        split.label(text="Slack:")
        split.prop(props, "slack", text="")
        
        # Resolution
        split = box.split(factor=0.4)
        split.label(text="Resolution:")
        split.prop(props, "resolution", text="")
        
        # Length
        split = box.split(factor=0.4)
        split.label(text="Length:")
        sub = split.row(align=True)
        sub.prop(props, "length_min", text="Min")
        sub.prop(props, "length_max", text="Max")
        
        layout.separator()
        
        # Action
        row = layout.row()
        row.scale_y = 1.5
        row.operator("mesh.random_cables", text="Generate Cables", icon='CURVE_BEZCURVE')
