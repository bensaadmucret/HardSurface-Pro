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
Random Panels panel - Professional UI matching Random Slice style.
"""

import bpy
from bpy.types import Panel


class VIEW3D_PT_hardsurface_panels(Panel):
    """Random Panels panel"""
    bl_label = "Random Panels"
    bl_idname = "VIEW3D_PT_hardsurface_panels"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'HardSurface'
    bl_parent_id = "VIEW3D_PT_hardsurface_main"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        wm = context.window_manager
        
        if not hasattr(wm, 'random_panels_props'):
            return
        props = wm.random_panels_props
        
        # === SEED ===
        box = layout.box()
        row = box.row(align=True)
        row.prop(props, "seed", text="Seed")
        row.operator("hardsurface.randomize_seed", text="", icon='FILE_REFRESH')
        
        # === SOLVER ===
        box = layout.box()
        box.label(text="Solver", icon='MODIFIER')
        row = box.row(align=True)
        row.prop(props, "solver_mode", expand=True)
        
        box.separator()
        
        # Direction
        split = box.split(factor=0.35)
        split.label(text="Direction:")
        split.prop(props, "direction_mode", expand=True)
        
        # Axis
        split = box.split(factor=0.35)
        split.label(text="Axis:")
        split.prop(props, "axis_mode", expand=True)
        
        # View mode
        split = box.split(factor=0.35)
        split.label(text="View:")
        split.prop(props, "view_mode", expand=True)
        
        # === CUTS (Inset / Depth) ===
        box = layout.box()
        box.label(text="Cuts", icon='MOD_BEVEL')
        
        # Probability
        split = box.split(factor=0.4)
        split.label(text="Probability:")
        split.prop(props, "probability", text="")
        
        # Inset Min/Max
        split = box.split(factor=0.4)
        split.label(text="Inset:")
        sub = split.row(align=True)
        sub.prop(props, "inset_min", text="Min")
        sub.prop(props, "inset_max", text="Max")
        
        # Depth Min/Max
        split = box.split(factor=0.4)
        split.label(text="Depth:")
        sub = split.row(align=True)
        sub.prop(props, "depth_min", text="Min")
        sub.prop(props, "depth_max", text="Max")
        
        # Safety Margin
        split = box.split(factor=0.4)
        split.label(text="Safety:")
        split.prop(props, "safety_margin", text="")
        
        # === EXTRUDE (Visual Polish) ===
        box = layout.box()
        box.label(text="Extrude", icon='MESH_DATA')
        
        # Use Copy toggle
        split = box.split(factor=0.4)
        split.label(text="Mode:")
        split.prop(props, "use_copy", text="Use Copy")
        
        # Materials toggle
        split = box.split(factor=0.4)
        split.label(text="Materials:")
        split.prop(props, "use_materials", text="Valley")
        
        # Bevel
        split = box.split(factor=0.4)
        split.label(text="Bevel:")
        split.prop(props, "bevel_amount", text="")
        
        layout.separator()
        
        # === ACTION BUTTON ===
        row = layout.row()
        row.scale_y = 1.5
        row.operator("mesh.random_panels", text="Generate Panels", icon='MESH_PLANE')
