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
Random Loop Extrude operator (Greeble Stacks).
Recursively insets and extrudes selected faces.
"""

import bpy
from bpy.types import Operator
from ...core.generators.loop_extrude_generator import LoopExtrudeGenerator
from ...services.selection_service import SelectionService
from ...services.seed_service import SeedService
from ...utils.blender_utils import BlenderUtils


class OBJECT_OT_random_loop_extrude(Operator):
    """Generate recursive greeble stacks on selected faces"""
    bl_idname = "mesh.random_loop_extrude"
    bl_label = "Random Loop Extrude"
    bl_options = {'REGISTER', 'UNDO'}
    
    seed: bpy.props.IntProperty(name="Seed", default=0, min=0)
    iterations: bpy.props.IntProperty(name="Iterations", default=2, min=1, max=6)
    probability: bpy.props.FloatProperty(name="Probability", default=0.7, min=0.0, max=1.0)
    height_min: bpy.props.FloatProperty(name="Height Min", default=0.05, min=0.0, max=1.0)
    height_max: bpy.props.FloatProperty(name="Height Max", default=0.3, min=0.0, max=1.0)
    height_decay: bpy.props.FloatProperty(name="Height Decay", default=0.7, min=0.1, max=1.0)
    inset_min: bpy.props.FloatProperty(name="Inset Min", default=0.02, min=0.0, max=1.0)
    inset_max: bpy.props.FloatProperty(name="Inset Max", default=0.1, min=0.0, max=1.0)
    taper: bpy.props.FloatProperty(name="Taper", default=0.0, min=0.0, max=1.0)
    use_copy: bpy.props.BoolProperty(name="Use Copy", default=False)
    
    def invoke(self, context, event):
        wm = context.window_manager
        if hasattr(wm, 'random_loop_extrude_props'):
            props = wm.random_loop_extrude_props
            self.seed = props.seed
            self.iterations = props.iterations
            self.probability = props.probability
            self.height_min = props.height_min
            self.height_max = props.height_max
            self.height_decay = props.height_decay
            self.inset_min = props.inset_min
            self.inset_max = props.inset_max
            self.taper = props.taper
            self.use_copy = props.use_copy
        return self.execute(context)
    
    def execute(self, context):
        obj = context.active_object
        is_valid, error = SelectionService.validate_face_selection(obj)
        if not is_valid:
            BlenderUtils.report_error(self, error)
            return {'CANCELLED'}
        
        wm = context.window_manager
        if hasattr(wm, 'random_loop_extrude_props'):
            props = wm.random_loop_extrude_props
            props.seed = self.seed
            props.iterations = self.iterations
            props.probability = self.probability
            props.height_min = self.height_min
            props.height_max = self.height_max
            props.height_decay = self.height_decay
            props.inset_min = self.inset_min
            props.inset_max = self.inset_max
            props.taper = self.taper
            props.use_copy = self.use_copy
        
        if hasattr(context.scene, 'hardsurface_props'):
            context.scene.hardsurface_props.last_operator_seed = self.seed
            context.scene.hardsurface_props.last_operator_type = "random_loop_extrude"
        
        generator = LoopExtrudeGenerator(self.seed)
        success, message = generator.generate(
            obj, self.iterations, self.probability,
            self.height_min, self.height_max, self.height_decay,
            self.inset_min, self.inset_max, self.taper, self.use_copy
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
        layout.prop(self, "iterations")
        layout.prop(self, "probability")
        layout.separator()
        layout.prop(self, "height_min")
        layout.prop(self, "height_max")
        layout.prop(self, "height_decay")
        layout.separator()
        layout.prop(self, "inset_min")
        layout.prop(self, "inset_max")
        layout.prop(self, "taper")
        layout.prop(self, "use_copy")
