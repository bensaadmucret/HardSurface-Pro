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
Load Preset operator.
Loads a preset and applies its parameters.
"""

import bpy
from bpy.types import Operator
from bpy.props import EnumProperty
from ...services.preset_service import PresetService
from ...utils.blender_utils import BlenderUtils


class OBJECT_OT_load_preset(Operator):
    """Load a preset"""
    bl_idname = "hardsurface.load_preset"
    bl_label = "Load Preset"
    bl_options = {'REGISTER'}
    
    preset_name: EnumProperty(
        name="Preset",
        description="Select a preset to load",
        items=lambda self, context: PresetService._get_preset_enum_items()
    )
    
    @staticmethod
    def _get_preset_enum_items():
        """Get enum items for preset selection."""
        presets = PresetService.list_presets()
        items = []
        for preset in presets:
            items.append((preset, preset, f"Load {preset}"))
        if not items:
            items.append(('NONE', 'No presets', 'No presets available'))
        return items
    
    def invoke(self, context, event):
        """Show preset selection dialog."""
        presets = PresetService.list_presets()
        if not presets:
            BlenderUtils.report_error(self, "No presets available")
            return {'CANCELLED'}
        return context.window_manager.invoke_props_dialog(self)
    
    def execute(self, context):
        """Load and apply the preset."""
        if self.preset_name == 'NONE':
            return {'CANCELLED'}
        
        preset_dict = PresetService.load_preset(self.preset_name)
        if preset_dict is None:
            BlenderUtils.report_error(self, "Failed to load preset")
            return {'CANCELLED'}
        
        # Apply parameters to appropriate property group
        wm = context.window_manager
        operator_type = preset_dict['operator_type']
        parameters = preset_dict['parameters']
        
        if operator_type == "random_panels" and hasattr(wm, 'random_panels_props'):
            props = wm.random_panels_props
            for key, value in parameters.items():
                if hasattr(props, key):
                    setattr(props, key, value)
        elif operator_type == "random_extrude" and hasattr(wm, 'random_extrude_props'):
            props = wm.random_extrude_props
            for key, value in parameters.items():
                if hasattr(props, key):
                    setattr(props, key, value)
        elif operator_type == "random_scatter" and hasattr(wm, 'random_scatter_props'):
            props = wm.random_scatter_props
            for key, value in parameters.items():
                if hasattr(props, key):
                    setattr(props, key, value)
        elif operator_type == "random_tubes" and hasattr(wm, 'random_tubes_props'):
            props = wm.random_tubes_props
            for key, value in parameters.items():
                if hasattr(props, key):
                    setattr(props, key, value)
        
        BlenderUtils.report_info(self, f"Preset '{self.preset_name}' loaded")
        return {'FINISHED'}
