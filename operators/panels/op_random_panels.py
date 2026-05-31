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
Random Panels operator.
Blender operator for generating random panels on selected faces.
"""

import bpy
from bpy.types import Operator
from ...core.generators.panels_generator import PanelsGenerator
from ...services.selection_service import SelectionService
from ...services.seed_service import SeedService
from ...properties.operator_props import RandomPanelsProps
from ...utils.blender_utils import BlenderUtils
from ...utils.logging import Logger


class OBJECT_OT_random_panels(Operator):
    """Generate random panels on selected faces"""
    bl_idname = "mesh.random_panels"
    bl_label = "Random Panels"
    bl_options = {'REGISTER', 'UNDO'}
    
    # Operator properties
    seed: bpy.props.IntProperty(
        name="Seed",
        description="Random seed for reproducible results",
        default=0,
        min=0
    )
    
    probability: bpy.props.FloatProperty(
        name="Probability",
        description="Probability of applying panel to each face",
        default=0.5,
        min=0.0,
        max=1.0
    )
    
    inset_min: bpy.props.FloatProperty(
        name="Inset Min",
        description="Minimum inset amount",
        default=0.02,
        min=0.0,
        max=1.0
    )
    
    inset_max: bpy.props.FloatProperty(
        name="Inset Max",
        description="Maximum inset amount",
        default=0.1,
        min=0.0,
        max=1.0
    )
    
    depth_min: bpy.props.FloatProperty(
        name="Depth Min",
        description="Minimum extrusion depth",
        default=-0.05,
        min=-1.0,
        max=1.0
    )
    
    depth_max: bpy.props.FloatProperty(
        name="Depth Max",
        description="Maximum extrusion depth",
        default=0.05,
        min=-1.0,
        max=1.0
    )
    
    safety_margin: bpy.props.FloatProperty(
        name="Safety Margin",
        description="Margin to avoid visual collisions",
        default=0.01,
        min=0.0,
        max=0.5
    )
    
    use_copy: bpy.props.BoolProperty(
        name="Use Copy",
        description="Apply on a copy of the object",
        default=False
    )
    
    use_materials: bpy.props.BoolProperty(
        name="Valley Materials",
        description="Assign second material slot to panel valleys",
        default=True
    )
    
    bevel_amount: bpy.props.FloatProperty(
        name="Bevel Amount",
        description="Bevel width for panel cap edges",
        default=0.0,
        min=0.0,
        max=0.1
    )
    
    def invoke(self, context, event):
        """Called when operator is invoked from UI."""
        # Load values from window manager properties if available
        wm = context.window_manager
        if hasattr(wm, 'random_panels_props'):
            props = wm.random_panels_props
            self.seed = props.seed
            self.probability = props.probability
            self.inset_min = props.inset_min
            self.inset_max = props.inset_max
            self.depth_min = props.depth_min
            self.depth_max = props.depth_max
            self.safety_margin = props.safety_margin
            self.use_copy = props.use_copy
            self.use_materials = props.use_materials
            self.bevel_amount = props.bevel_amount
        
        return self.execute(context)
    
    def execute(self, context):
        """Execute the random panels operation."""
        obj = context.active_object
        
        # Validate
        is_valid, error = SelectionService.validate_face_selection(obj)
        if not is_valid:
            BlenderUtils.report_error(self, error)
            return {'CANCELLED'}
        
        # Save properties to window manager
        wm = context.window_manager
        if hasattr(wm, 'random_panels_props'):
            props = wm.random_panels_props
            props.seed = self.seed
            props.probability = self.probability
            props.inset_min = self.inset_min
            props.inset_max = self.inset_max
            props.depth_min = self.depth_min
            props.depth_max = self.depth_max
            props.safety_margin = self.safety_margin
            props.use_copy = self.use_copy
            props.use_materials = self.use_materials
            props.bevel_amount = self.bevel_amount
        
        # Save to scene for rebuild
        if hasattr(context.scene, 'hardsurface_props'):
            context.scene.hardsurface_props.last_operator_seed = self.seed
            context.scene.hardsurface_props.last_operator_type = "random_panels"
        
        # Generate
        generator = PanelsGenerator(self.seed)
        success, message = generator.generate(
            obj,
            self.probability,
            self.inset_min,
            self.inset_max,
            self.depth_min,
            self.depth_max,
            self.safety_margin,
            self.use_copy,
            self.use_materials,
            self.bevel_amount
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
        layout.prop(self, "probability")
        layout.separator()
        layout.prop(self, "inset_min")
        layout.prop(self, "inset_max")
        layout.separator()
        layout.prop(self, "depth_min")
        layout.prop(self, "depth_max")
        layout.separator()
        layout.prop(self, "safety_margin")
        layout.prop(self, "use_copy")
        layout.separator()
        layout.prop(self, "use_materials")
        layout.prop(self, "bevel_amount")
