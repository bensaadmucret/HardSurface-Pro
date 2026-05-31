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
Random Tubes operator.
Blender operator for generating tubes from selected edges.
"""

import bpy
from bpy.types import Operator
from ...core.generators.tubes_generator import TubesGenerator
from ...services.selection_service import SelectionService
from ...properties.operator_props import RandomTubesProps
from ...utils.blender_utils import BlenderUtils


class OBJECT_OT_random_tubes(Operator):
    """Generate tubes from selected edges"""
    bl_idname = "mesh.random_tubes"
    bl_label = "Random Tubes"
    bl_options = {'REGISTER', 'UNDO'}
    
    # Operator properties
    seed: bpy.props.IntProperty(
        name="Seed",
        description="Random seed for reproducible results",
        default=0,
        min=0
    )
    
    radius: bpy.props.FloatProperty(
        name="Radius",
        description="Base radius of tubes",
        default=0.1,
        min=0.01,
        max=10.0
    )
    
    radius_variation: bpy.props.FloatProperty(
        name="Radius Variation",
        description="Amount of radius variation",
        default=0.5,
        min=0.0,
        max=1.0
    )
    
    segments: bpy.props.IntProperty(
        name="Segments",
        description="Number of segments per tube",
        default=16,
        min=3,
        max=64
    )
    
    smooth: bpy.props.BoolProperty(
        name="Smooth",
        description="Apply smooth shading to tubes",
        default=True
    )
    
    def invoke(self, context, event):
        """Called when operator is invoked from UI."""
        # Load values from window manager properties if available
        wm = context.window_manager
        if hasattr(wm, 'random_tubes_props'):
            props = wm.random_tubes_props
            self.seed = props.seed
            self.radius = props.radius
            self.radius_variation = props.radius_variation
            self.segments = props.segments
            self.smooth = props.smooth
        
        return self.execute(context)
    
    def execute(self, context):
        """Execute the random tubes operation."""
        obj = context.active_object
        
        # Validate
        is_valid, error = SelectionService.validate_mesh_object(obj)
        if not is_valid:
            BlenderUtils.report_error(self, error)
            return {'CANCELLED'}
        
        if obj.mode != 'EDIT':
            BlenderUtils.report_error(self, "Object must be in Edit Mode with edges selected")
            return {'CANCELLED'}
        
        # Save properties to window manager
        wm = context.window_manager
        if hasattr(wm, 'random_tubes_props'):
            props = wm.random_tubes_props
            props.seed = self.seed
            props.radius = self.radius
            props.radius_variation = props.radius_variation
            props.segments = props.segments
            props.smooth = props.smooth
        
        # Save to scene for rebuild
        if hasattr(context.scene, 'hardsurface_props'):
            context.scene.hardsurface_props.last_operator_seed = self.seed
            context.scene.hardsurface_props.last_operator_type = "random_tubes"
        
        # Generate
        generator = TubesGenerator(self.seed)
        success, message = generator.generate(
            obj,
            self.radius,
            self.radius_variation,
            self.segments,
            self.smooth
        )
        
        if success:
            BlenderUtils.report_info(self, message)
            return {'FINISHED'}
        else:
            BlenderUtils.report_error(self, message)
            return {'CANCELLED'}
    
    def draw(self, context):
        """Draw operator UI in redo panel."""
        layout = self.layout
        layout.prop(self, "seed")
        layout.separator()
        layout.prop(self, "radius")
        layout.prop(self, "radius_variation")
        layout.prop(self, "segments")
        layout.prop(self, "smooth")
