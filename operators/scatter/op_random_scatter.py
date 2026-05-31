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
Random Scatter operator.
Blender operator for scattering objects from a collection on a target surface.
"""

import bpy
from bpy.types import Operator
from ...core.generators.scatter_generator import ScatterGenerator
from ...services.selection_service import SelectionService
from ...properties.operator_props import RandomScatterProps
from ...utils.blender_utils import BlenderUtils


class OBJECT_OT_random_scatter(Operator):
    """Scatter objects from a collection on the target surface"""
    bl_idname = "mesh.random_scatter"
    bl_label = "Random Scatter"
    bl_options = {'REGISTER', 'UNDO'}
    
    # Operator properties
    seed: bpy.props.IntProperty(
        name="Seed",
        description="Random seed for reproducible results",
        default=0,
        min=0
    )
    
    collection_name: bpy.props.StringProperty(
        name="Collection",
        description="Source collection of objects to scatter",
        default=""
    )
    
    density: bpy.props.FloatProperty(
        name="Density",
        description="Number of objects per unit area",
        default=1.0,
        min=0.1,
        max=100.0
    )
    
    rotation_min: bpy.props.FloatProperty(
        name="Rotation Min",
        description="Minimum random rotation (degrees)",
        default=0.0,
        min=0.0,
        max=360.0
    )
    
    rotation_max: bpy.props.FloatProperty(
        name="Rotation Max",
        description="Maximum random rotation (degrees)",
        default=360.0,
        min=0.0,
        max=360.0
    )
    
    scale_min: bpy.props.FloatProperty(
        name="Scale Min",
        description="Minimum random scale",
        default=0.5,
        min=0.1,
        max=10.0
    )
    
    scale_max: bpy.props.FloatProperty(
        name="Scale Max",
        description="Maximum random scale",
        default=1.5,
        min=0.1,
        max=10.0
    )
    
    align_to_normal: bpy.props.BoolProperty(
        name="Align to Normal",
        description="Align objects to surface normal",
        default=True
    )
    
    surface_offset: bpy.props.FloatProperty(
        name="Surface Offset",
        description="Offset from surface",
        default=0.0,
        min=-10.0,
        max=10.0
    )
    
    def invoke(self, context, event):
        """Called when operator is invoked from UI."""
        # Load values from window manager properties if available
        wm = context.window_manager
        if hasattr(wm, 'random_scatter_props'):
            props = wm.random_scatter_props
            self.seed = props.seed
            self.collection_name = props.collection_name
            self.density = props.density
            self.rotation_min = props.rotation_min
            self.rotation_max = props.rotation_max
            self.scale_min = props.scale_min
            self.scale_max = props.scale_max
            self.align_to_normal = props.align_to_normal
            self.surface_offset = props.surface_offset
        
        return self.execute(context)
    
    def execute(self, context):
        """Execute the random scatter operation."""
        obj = context.active_object
        
        # Validate
        is_valid, error = SelectionService.validate_mesh_object(obj)
        if not is_valid:
            BlenderUtils.report_error(self, error)
            return {'CANCELLED'}
        
        if not self.collection_name:
            BlenderUtils.report_error(self, "Please select a collection")
            return {'CANCELLED'}
        
        # Save properties to window manager
        wm = context.window_manager
        if hasattr(wm, 'random_scatter_props'):
            props = wm.random_scatter_props
            props.seed = self.seed
            props.collection_name = self.collection_name
            props.density = self.density
            props.rotation_min = self.rotation_min
            props.rotation_max = self.rotation_max
            props.scale_min = self.scale_min
            props.scale_max = self.scale_max
            props.align_to_normal = self.align_to_normal
            props.surface_offset = self.surface_offset
        
        # Save to scene for rebuild
        if hasattr(context.scene, 'hardsurface_props'):
            context.scene.hardsurface_props.last_operator_seed = self.seed
            context.scene.hardsurface_props.last_operator_type = "random_scatter"
        
        # Generate
        generator = ScatterGenerator(self.seed)
        success, message = generator.generate(
            obj,
            self.collection_name,
            self.density,
            self.rotation_min,
            self.rotation_max,
            self.scale_min,
            self.scale_max,
            self.align_to_normal,
            self.surface_offset
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
        layout.prop_search(self, "collection_name", bpy.data, "collections")
        layout.separator()
        layout.prop(self, "density")
        layout.separator()
        layout.prop(self, "rotation_min")
        layout.prop(self, "rotation_max")
        layout.separator()
        layout.prop(self, "scale_min")
        layout.prop(self, "scale_max")
        layout.separator()
        layout.prop(self, "align_to_normal")
        layout.prop(self, "surface_offset")
