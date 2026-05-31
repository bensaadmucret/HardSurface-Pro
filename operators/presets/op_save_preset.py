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
Save Preset operator.
Saves current operator parameters as a preset.
"""

import bpy
from bpy.types import Operator
from bpy.props import StringProperty
from ...services.preset_service import PresetService
from ...utils.blender_utils import BlenderUtils


class OBJECT_OT_save_preset(Operator):
    """Save current settings as a preset"""
    bl_idname = "hardsurface.save_preset"
    bl_label = "Save Preset"
    bl_options = {'REGISTER'}
    
    preset_name: StringProperty(
        name="Preset Name",
        description="Name for the preset",
        default="My Preset"
    )
    
    def invoke(self, context, event):
        """Show input dialog for preset name."""
        return context.window_manager.invoke_props_dialog(self)
    
    def execute(self, context):
        """Save the preset."""
        wm = context.window_manager
        
        # Determine which operator type to save based on last operator
        if hasattr(context.scene, 'hardsurface_props'):
            last_type = context.scene.hardsurface_props.last_operator_type
        else:
            last_type = "random_panels"  # Default
        
        # Get parameters from appropriate property group
        parameters = {}
        if last_type == "random_panels" and hasattr(wm, 'random_panels_props'):
            props = wm.random_panels_props
            parameters = {
                'seed': props.seed,
                'probability': props.probability,
                'inset_min': props.inset_min,
                'inset_max': props.inset_max,
                'depth_min': props.depth_min,
                'depth_max': props.depth_max,
                'safety_margin': props.safety_margin,
                'use_copy': props.use_copy
            }
        elif last_type == "random_extrude" and hasattr(wm, 'random_extrude_props'):
            props = wm.random_extrude_props
            parameters = {
                'seed': props.seed,
                'extrude_rate': props.extrude_rate,
                'height_min': props.height_min,
                'height_max': props.height_max,
                'taper_min': props.taper_min,
                'taper_max': props.taper_max,
                'max_faces': props.max_faces,
                'group_islands': props.group_islands
            }
        elif last_type == "random_scatter" and hasattr(wm, 'random_scatter_props'):
            props = wm.random_scatter_props
            parameters = {
                'seed': props.seed,
                'collection_name': props.collection_name,
                'density': props.density,
                'rotation_min': props.rotation_min,
                'rotation_max': props.rotation_max,
                'scale_min': props.scale_min,
                'scale_max': props.scale_max,
                'align_to_normal': props.align_to_normal,
                'surface_offset': props.surface_offset
            }
        elif last_type == "random_tubes" and hasattr(wm, 'random_tubes_props'):
            props = wm.random_tubes_props
            parameters = {
                'seed': props.seed,
                'radius': props.radius,
                'radius_variation': props.radius_variation,
                'segments': props.segments,
                'smooth': props.smooth
            }
        else:
            BlenderUtils.report_error(self, "No valid operator parameters to save")
            return {'CANCELLED'}
        
        # Save preset
        if PresetService.save_preset(self.preset_name, last_type, parameters):
            BlenderUtils.report_info(self, f"Preset '{self.preset_name}' saved")
            return {'FINISHED'}
        else:
            BlenderUtils.report_error(self, "Failed to save preset")
            return {'CANCELLED'}
