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
Flanges/Couplings panel for the N-Panel sidebar.
"""

import bpy
from bpy.types import Panel


class VIEW3D_PT_hardsurface_flanges(Panel):
    """Flanges/Couplings panel"""
    bl_label = "Flanges / Couplings"
    bl_idname = "VIEW3D_PT_hardsurface_flanges"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "HardSurface"
    bl_parent_id = "VIEW3D_PT_hardsurface_main"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj is not None and obj.type == 'CURVE'

    def draw(self, context):
        layout = self.layout
        wm = context.window_manager
        
        if not hasattr(wm, 'flanges_props'):
            return
        props = wm.flanges_props
        
        # Seed
        box = layout.box()
        row = box.row(align=True)
        row.prop(props, "seed", text="Seed")
        row.operator("hardsurface.randomize_seed", text="", icon='FILE_REFRESH')
        
        # Flange Size
        box = layout.box()
        box.label(text="Flange Dimensions", icon='MESH_CYLINDER')
        split = box.split(factor=0.4)
        split.label(text="Size:")
        split.prop(props, "flange_size", text="")
        
        split = box.split(factor=0.4)
        split.label(text="Depth:")
        split.prop(props, "flange_depth", text="")
        
        # Distribution
        box = layout.box()
        box.label(text="Distribution", icon='PARTICLES')
        split = box.split(factor=0.4)
        split.label(text="Spacing:")
        split.prop(props, "spacing", text="")
        
        split = box.split(factor=0.4)
        split.label(text="Probability:")
        split.prop(props, "probability", text="")
        
        # Options
        box = layout.box()
        box.label(text="Options", icon='PREFERENCES')
        split = box.split(factor=0.4)
        split.label(text="Mode:")
        split.prop(props, "use_existing_curve", text="Existing Curve")
        
        layout.separator()
        
        # Action
        row = layout.row()
        row.scale_y = 1.5
        row.operator("mesh.flanges", text="Generate Flanges", icon='MESH_CYLINDER')
