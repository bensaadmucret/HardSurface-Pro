# HardSurface Pro - Procedural Hard-Surface Generation Addon for Blender
# Copyright (C) 2024 HardSurface Pro Contributors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

"""
Random Extrude operator.
Blender operator for generating random extrusions on selected faces.
"""

import bpy
from bpy.types import Operator
from ...core.generators.extrude_generator import ExtrudeGenerator
from ...services.selection_service import SelectionService
from ...services.seed_service import SeedService
from ...properties.operator_props import RandomExtrudeProps
from ...utils.blender_utils import BlenderUtils
from ...utils.logging import Logger


class OBJECT_OT_random_extrude(Operator):
    """Generate random extrusions on selected faces"""
    bl_idname = "mesh.random_extrude"
    bl_label = "Random Extrude"
    bl_options = {'REGISTER', 'UNDO'}
    
    # Operator properties
    seed: bpy.props.IntProperty(
        name="Seed",
        description="Random seed for reproducible results",
        default=0,
        min=0
    )
    
    extrude_rate: bpy.props.FloatProperty(
        name="Extrude Rate",
        description="Rate of face extrusion",
        default=0.5,
        min=0.0,
        max=1.0
    )
    
    height_min: bpy.props.FloatProperty(
        name="Height Min",
        description="Minimum extrusion height",
        default=0.2,
        min=0.0,
        max=10.0
    )
    
    height_max: bpy.props.FloatProperty(
        name="Height Max",
        description="Maximum extrusion height",
        default=1.0,
        min=0.0,
        max=10.0
    )
    
    taper_min: bpy.props.FloatProperty(
        name="Taper Min",
        description="Minimum taper amount (0 = no taper)",
        default=0.0,
        min=0.0,
        max=1.0
    )
    
    taper_max: bpy.props.FloatProperty(
        name="Taper Max",
        description="Maximum taper amount (1 = point, 0 = no taper)",
        default=0.2,
        min=0.0,
        max=1.0
    )
    
    max_faces: bpy.props.IntProperty(
        name="Max Faces",
        description="Maximum number of faces to affect",
        default=100,
        min=1,
        max=10000
    )
    
    group_islands: bpy.props.BoolProperty(
        name="Group Islands",
        description="Group affected faces by islands",
        default=False
    )
    
    def invoke(self, context, event):
        """Called when operator is invoked from UI."""
        # Load values from window manager properties if available
        wm = context.window_manager
        if hasattr(wm, 'random_extrude_props'):
            props = wm.random_extrude_props
            self.seed = props.seed
            self.extrude_rate = props.extrude_rate
            self.height_min = props.height_min
            self.height_max = props.height_max
            self.taper_min = props.taper_min
            self.taper_max = props.taper_max
            self.max_faces = props.max_faces
            self.group_islands = props.group_islands
        
        return self.execute(context)
    
    def execute(self, context):
        """Execute the random extrude operation."""
        obj = context.active_object
        
        # Validate
        is_valid, error = SelectionService.validate_face_selection(obj)
        if not is_valid:
            BlenderUtils.report_error(self, error)
            return {'CANCELLED'}
        
        # Save properties to window manager
        wm = context.window_manager
        if hasattr(wm, 'random_extrude_props'):
            props = wm.random_extrude_props
            props.seed = self.seed
            props.extrude_rate = self.extrude_rate
            props.height_min = self.height_min
            props.height_max = self.height_max
            props.taper_min = self.taper_min
            props.taper_max = self.taper_max
            props.max_faces = self.max_faces
            props.group_islands = self.group_islands
        
        # Save to scene for rebuild
        if hasattr(context.scene, 'hardsurface_props'):
            context.scene.hardsurface_props.last_operator_seed = self.seed
            context.scene.hardsurface_props.last_operator_type = "random_extrude"
        
        # Generate
        generator = ExtrudeGenerator(self.seed)
        success, message = generator.generate(
            obj,
            self.extrude_rate,
            self.height_min,
            self.height_max,
            self.taper_min,
            self.taper_max,
            self.max_faces,
            self.group_islands
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
        layout.prop(self, "extrude_rate")
        layout.separator()
        layout.prop(self, "height_min")
        layout.prop(self, "height_max")
        layout.separator()
        layout.prop(self, "taper_min")
        layout.prop(self, "taper_max")
        layout.separator()
        layout.prop(self, "max_faces")
        layout.prop(self, "group_islands")
