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
Random Cables operator.
Creates catenary or bezier curves as cables.
"""

import bpy
from bpy.types import Operator
from ...core.generators.cables_generator import CablesGenerator
from ...utils.blender_utils import BlenderUtils


class OBJECT_OT_random_cables(Operator):
    """Generate random cables as curves"""
    bl_idname = "mesh.random_cables"
    bl_label = "Random Cables"
    bl_options = {'REGISTER', 'UNDO'}
    
    seed: bpy.props.IntProperty(name="Seed", default=0, min=0)
    cable_type: bpy.props.EnumProperty(
        name="Cable Type",
        items=[
            ('CATENARY', "Catenary", "Hanging cable curve"),
            ('BEZIER', "Bezier", "Manual bezier curve"),
            ('STRAIGHT', "Straight", "Straight line cable"),
        ],
        default='CATENARY'
    )
    count: bpy.props.IntProperty(name="Count", default=3, min=1, max=50)
    radius: bpy.props.FloatProperty(name="Radius", default=0.02, min=0.001, max=0.5)
    slack: bpy.props.FloatProperty(name="Slack", default=0.3, min=0.0, max=2.0)
    resolution: bpy.props.IntProperty(name="Resolution", default=12, min=3, max=64)
    length_min: bpy.props.FloatProperty(name="Length Min", default=1.0, min=0.1, max=10.0)
    length_max: bpy.props.FloatProperty(name="Length Max", default=3.0, min=0.1, max=10.0)
    
    def invoke(self, context, event):
        wm = context.window_manager
        if hasattr(wm, 'random_cables_props'):
            p = wm.random_cables_props
            self.seed = p.seed
            self.cable_type = p.cable_type
            self.count = p.count
            self.radius = p.radius
            self.slack = p.slack
            self.resolution = p.resolution
            self.length_min = p.length_min
            self.length_max = p.length_max
        return self.execute(context)
    
    def execute(self, context):
        obj = context.active_object
        
        wm = context.window_manager
        if hasattr(wm, 'random_cables_props'):
            p = wm.random_cables_props
            p.seed = self.seed
            p.cable_type = self.cable_type
            p.count = self.count
            p.radius = self.radius
            p.slack = self.slack
            p.resolution = self.resolution
            p.length_min = self.length_min
            p.length_max = self.length_max
        
        if hasattr(context.scene, 'hardsurface_props'):
            context.scene.hardsurface_props.last_operator_seed = self.seed
            context.scene.hardsurface_props.last_operator_type = "random_cables"
        
        generator = CablesGenerator(self.seed)
        success, message = generator.generate(
            obj, self.cable_type, self.count, self.radius,
            self.slack, self.resolution, self.length_min, self.length_max
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
        layout.prop(self, "cable_type")
        layout.prop(self, "count")
        layout.prop(self, "radius")
        layout.prop(self, "slack")
        layout.prop(self, "resolution")
        layout.prop(self, "length_min")
        layout.prop(self, "length_max")
