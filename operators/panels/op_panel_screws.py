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
Panel Screws operator.
Places mechanical screws at the corners of selected faces.
"""

import bpy
from bpy.types import Operator
from ...core.generators.screws_generator import ScrewsGenerator
from ...services.selection_service import SelectionService
from ...services.seed_service import SeedService
from ...utils.blender_utils import BlenderUtils


class OBJECT_OT_panel_screws(Operator):
    """Place screws at corners of selected faces"""
    bl_idname = "mesh.panel_screws"
    bl_label = "Panel Screws"
    bl_options = {'REGISTER', 'UNDO'}
    
    seed: bpy.props.IntProperty(name="Seed", default=0, min=0)
    screw_size: bpy.props.FloatProperty(name="Screw Size", default=0.02, min=0.001, max=0.5)
    screw_depth: bpy.props.FloatProperty(name="Screw Depth", default=0.005, min=0.0, max=0.1)
    probability: bpy.props.FloatProperty(name="Probability", default=0.8, min=0.0, max=1.0)
    screw_type: bpy.props.IntProperty(name="Screw Type", default=0, min=0, max=2)
    
    def invoke(self, context, event):
        wm = context.window_manager
        if hasattr(wm, 'panel_screws_props'):
            props = wm.panel_screws_props
            self.seed = props.seed
            self.screw_size = props.screw_size
            self.screw_depth = props.screw_depth
            self.probability = props.probability
            self.screw_type = props.screw_type
        return self.execute(context)
    
    def execute(self, context):
        obj = context.active_object
        is_valid, error = SelectionService.validate_face_selection(obj)
        if not is_valid:
            BlenderUtils.report_error(self, error)
            return {'CANCELLED'}
        
        wm = context.window_manager
        if hasattr(wm, 'panel_screws_props'):
            props = wm.panel_screws_props
            props.seed = self.seed
            props.screw_size = self.screw_size
            props.screw_depth = self.screw_depth
            props.probability = self.probability
            props.screw_type = self.screw_type
        
        if hasattr(context.scene, 'hardsurface_props'):
            context.scene.hardsurface_props.last_operator_seed = self.seed
            context.scene.hardsurface_props.last_operator_type = "panel_screws"
        
        generator = ScrewsGenerator(self.seed)
        success, message = generator.generate(
            obj, self.screw_size, self.screw_depth, self.probability, self.screw_type
        )
        
        if success:
            BlenderUtils.report_info(self, message)
            return {'FINISHED'}
        else:
            BlenderUtils.report_error(self, message)
            return {'CANCELLED'}
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "seed")
        layout.prop(self, "screw_size")
        layout.prop(self, "screw_depth")
        layout.prop(self, "probability")
        layout.prop(self, "screw_type")
