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
Random Cells panel for the N-Panel sidebar.
"""

import bpy
from bpy.types import Panel


class VIEW3D_PT_hardsurface_cells(Panel):
    """Random Cells panel"""
    bl_label = "Random Cells"
    bl_idname = "VIEW3D_PT_hardsurface_cells"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "HardSurface"
    bl_parent_id = "VIEW3D_PT_hardsurface_main"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        wm = context.window_manager
        
        if not hasattr(wm, 'random_cells_props'):
            return
        props = wm.random_cells_props
        
        # Seed
        box = layout.box()
        row = box.row(align=True)
        row.prop(props, "seed", text="Seed")
        row.operator("hardsurface.randomize_seed", text="", icon='FILE_REFRESH')
        
        # Cell Type
        box = layout.box()
        box.label(text="Cell Type", icon='MESH_PLANE')
        row = box.row(align=True)
        row.prop(props, "cell_type", expand=True)
        
        # Density
        box = layout.box()
        box.label(text="Distribution", icon='PARTICLES')
        split = box.split(factor=0.4)
        split.label(text="Density:")
        split.prop(props, "density", text="")
        
        # Size
        split = box.split(factor=0.4)
        split.label(text="Size:")
        sub = split.row(align=True)
        sub.prop(props, "size_min", text="Min")
        sub.prop(props, "size_max", text="Max")
        
        # Height
        split = box.split(factor=0.4)
        split.label(text="Height:")
        sub = split.row(align=True)
        sub.prop(props, "height_min", text="Min")
        sub.prop(props, "height_max", text="Max")
        
        # Options
        box = layout.box()
        box.label(text="Options", icon='PREFERENCES')
        split = box.split(factor=0.4)
        split.label(text="Align:")
        split.prop(props, "align_to_normal", text="To Normal")
        split = box.split(factor=0.4)
        split.label(text="Mode:")
        split.prop(props, "use_copy", text="Use Copy")
        
        layout.separator()
        
        # Action
        row = layout.row()
        row.scale_y = 1.5
        row.operator("mesh.random_cells", text="Generate Cells", icon='MESH_GRID')
