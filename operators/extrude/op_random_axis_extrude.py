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
Random Axis Extrude operator.
Creates recursive branching extrusions in XYZ axis.
"""

import bpy
from bpy.types import Operator
from ...core.generators.axis_extrude_generator import AxisExtrudeGenerator
from ...services.selection_service import SelectionService
from ...utils.blender_utils import BlenderUtils


class OBJECT_OT_random_axis_extrude(Operator):
    """Generate recursive axis-aligned branching extrusions"""
    bl_idname = "mesh.random_axis_extrude"
    bl_label = "Random Axis Extrude"
    bl_options = {'REGISTER', 'UNDO'}
    
    seed: bpy.props.IntProperty(name="Seed", default=0, min=0)
    iterations: bpy.props.IntProperty(name="Iterations", default=2, min=1, max=5)
    probability_x: bpy.props.FloatProperty(name="X Prob", default=0.5, min=0.0, max=1.0)
    probability_y: bpy.props.FloatProperty(name="Y Prob", default=0.5, min=0.0, max=1.0)
    probability_z: bpy.props.FloatProperty(name="Z Prob", default=0.5, min=0.0, max=1.0)
    length_min: bpy.props.FloatProperty(name="Length Min", default=0.1, min=0.01, max=5.0)
    length_max: bpy.props.FloatProperty(name="Length Max", default=0.5, min=0.01, max=5.0)
    scale_decay: bpy.props.FloatProperty(name="Scale Decay", default=0.7, min=0.1, max=1.0)
    use_copy: bpy.props.BoolProperty(name="Use Copy", default=False)
    
    def invoke(self, context, event):
        wm = context.window_manager
        if hasattr(wm, 'random_axis_extrude_props'):
            p = wm.random_axis_extrude_props
            self.seed = p.seed
            self.iterations = p.iterations
            self.probability_x = p.probability_x
            self.probability_y = p.probability_y
            self.probability_z = p.probability_z
            self.length_min = p.length_min
            self.length_max = p.length_max
            self.scale_decay = p.scale_decay
            self.use_copy = p.use_copy
        return self.execute(context)
    
    def execute(self, context):
        obj = context.active_object
        is_valid, error = SelectionService.validate_face_selection(obj)
        if not is_valid:
            BlenderUtils.report_error(self, error)
            return {'CANCELLED'}
        
        wm = context.window_manager
        if hasattr(wm, 'random_axis_extrude_props'):
            p = wm.random_axis_extrude_props
            p.seed = self.seed
            p.iterations = self.iterations
            p.probability_x = self.probability_x
            p.probability_y = self.probability_y
            p.probability_z = self.probability_z
            p.length_min = self.length_min
            p.length_max = self.length_max
            p.scale_decay = self.scale_decay
            p.use_copy = self.use_copy
        
        if hasattr(context.scene, 'hardsurface_props'):
            context.scene.hardsurface_props.last_operator_seed = self.seed
            context.scene.hardsurface_props.last_operator_type = "random_axis_extrude"
        
        generator = AxisExtrudeGenerator(self.seed)
        success, message = generator.generate(
            obj, self.iterations,
            self.probability_x, self.probability_y, self.probability_z,
            self.length_min, self.length_max, self.scale_decay, self.use_copy
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
        layout.separator()
        layout.prop(self, "probability_x")
        layout.prop(self, "probability_y")
        layout.prop(self, "probability_z")
        layout.separator()
        layout.prop(self, "length_min")
        layout.prop(self, "length_max")
        layout.prop(self, "scale_decay")
        layout.prop(self, "use_copy")
