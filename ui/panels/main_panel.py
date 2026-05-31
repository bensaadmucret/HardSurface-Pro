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
Main panel for the HardSurface addon.
Root panel in the N-Panel containing all sub-panels.
"""

import bpy
from bpy.types import Panel


class VIEW3D_PT_hardsurface_main(Panel):
    """Main HardSurface Pro panel"""
    bl_label = "HardSurface Pro"
    bl_idname = "VIEW3D_PT_hardsurface_main"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'HardSurface'
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        """Draw the main panel."""
        layout = self.layout
        
        # Header info
        layout.label(text="Procedural Hard-Surface Generation", icon='MESH_ICOSPHERE')
        layout.separator()
        
        # Quick help box
        box = layout.box()
        box.label(text="Quick Tips:", icon='INFO')
        box.label(text="• Edit Mode + Select faces/edges")
        box.label(text="• Adjust seed for variations")
        box.label(text="• Use Presets to save settings")
        
        layout.separator()
        
        # Last operator info
        if hasattr(context.scene, 'hardsurface_props'):
            props = context.scene.hardsurface_props
            if props.last_operator_type:
                layout.label(text=f"Last: {props.last_operator_type}")
                layout.label(text=f"Seed: {props.last_operator_seed}")
        
        layout.separator()
