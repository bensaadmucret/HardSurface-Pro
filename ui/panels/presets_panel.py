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
Presets panel.
Sub-panel for preset management.
"""

import bpy
from bpy.types import Panel


class VIEW3D_PT_hardsurface_presets(Panel):
    """Presets panel"""
    bl_label = "Presets"
    bl_idname = "VIEW3D_PT_hardsurface_presets"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'HardSurface'
    bl_parent_id = "VIEW3D_PT_hardsurface_main"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        """Draw the Presets panel."""
        layout = self.layout
        
        layout.label(text="Preset Management", icon='PRESET')
        layout.separator()
        
        # Preset actions
        layout.operator("hardsurface.save_preset", icon='FILE_NEW')
        layout.operator("hardsurface.load_preset", icon='FILE_FOLDER')
        layout.operator("hardsurface.delete_preset", icon='X')
