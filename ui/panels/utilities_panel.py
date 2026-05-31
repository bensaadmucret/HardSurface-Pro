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
Utilities panel.
Sub-panel for common utilities like reset.
"""

import bpy
from bpy.types import Panel


class VIEW3D_PT_hardsurface_utilities(Panel):
    """Utilities panel"""
    bl_label = "Utilities"
    bl_idname = "VIEW3D_PT_hardsurface_utilities"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'HardSurface'
    bl_parent_id = "VIEW3D_PT_hardsurface_main"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        """Draw the Utilities panel."""
        layout = self.layout
        
        layout.label(text="Global Actions", icon='TOOL_SETTINGS')
        layout.separator()
        
        layout.operator("hardsurface.reset_settings", icon='X')
