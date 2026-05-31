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
Delete Preset operator.
Deletes a preset from the preset directory.
"""

import bpy
from bpy.types import Operator
from bpy.props import EnumProperty
from ...services.preset_service import PresetService
from ...utils.blender_utils import BlenderUtils


class OBJECT_OT_delete_preset(Operator):
    """Delete a preset"""
    bl_idname = "hardsurface.delete_preset"
    bl_label = "Delete Preset"
    bl_options = {'REGISTER'}
    
    preset_name: EnumProperty(
        name="Preset",
        description="Select a preset to delete",
        items=lambda self, context: PresetService._get_preset_enum_items()
    )
    
    @staticmethod
    def _get_preset_enum_items():
        """Get enum items for preset selection."""
        presets = PresetService.list_presets()
        items = []
        for preset in presets:
            items.append((preset, preset, f"Delete {preset}"))
        if not items:
            items.append(('NONE', 'No presets', 'No presets available'))
        return items
    
    def invoke(self, context, event):
        """Show preset selection dialog."""
        presets = PresetService.list_presets()
        if not presets:
            BlenderUtils.report_error(self, "No presets available")
            return {'CANCELLED'}
        return context.window_manager.invoke_confirm(self, event)
    
    def execute(self, context):
        """Delete the preset."""
        if self.preset_name == 'NONE':
            return {'CANCELLED'}
        
        if PresetService.delete_preset(self.preset_name):
            BlenderUtils.report_info(self, f"Preset '{self.preset_name}' deleted")
            return {'FINISHED'}
        else:
            BlenderUtils.report_error(self, "Failed to delete preset")
            return {'CANCELLED'}
