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
Flanges/Couplings operator.
Creates flange meshes along curves.
"""

import bpy
from bpy.types import Operator
from ...core.generators.flanges_generator import FlangesGenerator
from ...utils.blender_utils import BlenderUtils


class OBJECT_OT_flanges(Operator):
    """Generate flanges/couplings on selected curve"""
    bl_idname = "mesh.flanges"
    bl_label = "Flanges / Couplings"
    bl_options = {'REGISTER', 'UNDO'}
    
    seed: bpy.props.IntProperty(name="Seed", default=0, min=0)
    flange_size: bpy.props.FloatProperty(name="Flange Size", default=0.05, min=0.01, max=0.5)
    flange_depth: bpy.props.FloatProperty(name="Flange Depth", default=0.02, min=0.005, max=0.2)
    spacing: bpy.props.FloatProperty(name="Spacing", default=0.5, min=0.1, max=5.0)
    probability: bpy.props.FloatProperty(name="Probability", default=0.8, min=0.0, max=1.0)
    use_existing_curve: bpy.props.BoolProperty(name="Use Existing Curve", default=False)
    
    def invoke(self, context, event):
        wm = context.window_manager
        if hasattr(wm, 'flanges_props'):
            p = wm.flanges_props
            self.seed = p.seed
            self.flange_size = p.flange_size
            self.flange_depth = p.flange_depth
            self.spacing = p.spacing
            self.probability = p.probability
            self.use_existing_curve = p.use_existing_curve
        return self.execute(context)
    
    def execute(self, context):
        obj = context.active_object
        if obj is None or obj.type != 'CURVE':
            BlenderUtils.report_error(self, "Select a curve object")
            return {'CANCELLED'}
        
        wm = context.window_manager
        if hasattr(wm, 'flanges_props'):
            p = wm.flanges_props
            p.seed = self.seed
            p.flange_size = self.flange_size
            p.flange_depth = self.flange_depth
            p.spacing = self.spacing
            p.probability = self.probability
            p.use_existing_curve = self.use_existing_curve
        
        if hasattr(context.scene, 'hardsurface_props'):
            context.scene.hardsurface_props.last_operator_seed = self.seed
            context.scene.hardsurface_props.last_operator_type = "flanges"
        
        generator = FlangesGenerator(self.seed)
        success, message = generator.generate(
            obj, self.flange_size, self.flange_depth,
            self.spacing, self.probability, self.use_existing_curve
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
        layout.prop(self, "flange_size")
        layout.prop(self, "flange_depth")
        layout.prop(self, "spacing")
        layout.prop(self, "probability")
        layout.prop(self, "use_existing_curve")
