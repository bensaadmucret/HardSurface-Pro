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
Random Cells operator.
Creates emission planes or antenna-like structures.
"""

import bpy
from bpy.types import Operator
from ...core.generators.cells_generator import CellsGenerator
from ...services.selection_service import SelectionService
from ...utils.blender_utils import BlenderUtils


class OBJECT_OT_random_cells(Operator):
    """Generate cells (planes/antennae/boxes) on selected faces"""
    bl_idname = "mesh.random_cells"
    bl_label = "Random Cells"
    bl_options = {'REGISTER', 'UNDO'}
    
    seed: bpy.props.IntProperty(name="Seed", default=0, min=0)
    cell_type: bpy.props.EnumProperty(
        name="Cell Type",
        items=[
            ('PLANE', "Plane", "Flat emission plane"),
            ('ANTENNA', "Antenna", "Thin extruded antenna"),
            ('BOX', "Box", "Small box protrusion"),
        ],
        default='PLANE'
    )
    density: bpy.props.FloatProperty(name="Density", default=0.3, min=0.0, max=1.0)
    size_min: bpy.props.FloatProperty(name="Size Min", default=0.05, min=0.01, max=1.0)
    size_max: bpy.props.FloatProperty(name="Size Max", default=0.2, min=0.01, max=1.0)
    height_min: bpy.props.FloatProperty(name="Height Min", default=0.1, min=0.0, max=2.0)
    height_max: bpy.props.FloatProperty(name="Height Max", default=0.5, min=0.0, max=2.0)
    align_to_normal: bpy.props.BoolProperty(name="Align to Normal", default=True)
    use_copy: bpy.props.BoolProperty(name="Use Copy", default=False)
    
    def invoke(self, context, event):
        wm = context.window_manager
        if hasattr(wm, 'random_cells_props'):
            p = wm.random_cells_props
            self.seed = p.seed
            self.cell_type = p.cell_type
            self.density = p.density
            self.size_min = p.size_min
            self.size_max = p.size_max
            self.height_min = p.height_min
            self.height_max = p.height_max
            self.align_to_normal = p.align_to_normal
            self.use_copy = p.use_copy
        return self.execute(context)
    
    def execute(self, context):
        obj = context.active_object
        is_valid, error = SelectionService.validate_face_selection(obj)
        if not is_valid:
            BlenderUtils.report_error(self, error)
            return {'CANCELLED'}
        
        wm = context.window_manager
        if hasattr(wm, 'random_cells_props'):
            p = wm.random_cells_props
            p.seed = self.seed
            p.cell_type = self.cell_type
            p.density = self.density
            p.size_min = self.size_min
            p.size_max = self.size_max
            p.height_min = self.height_min
            p.height_max = self.height_max
            p.align_to_normal = self.align_to_normal
            p.use_copy = self.use_copy
        
        if hasattr(context.scene, 'hardsurface_props'):
            context.scene.hardsurface_props.last_operator_seed = self.seed
            context.scene.hardsurface_props.last_operator_type = "random_cells"
        
        generator = CellsGenerator(self.seed)
        success, message = generator.generate(
            obj, self.cell_type, self.density,
            self.size_min, self.size_max, self.height_min, self.height_max,
            self.align_to_normal, self.use_copy
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
        layout.prop(self, "cell_type")
        layout.prop(self, "density")
        layout.separator()
        layout.prop(self, "size_min")
        layout.prop(self, "size_max")
        layout.separator()
        layout.prop(self, "height_min")
        layout.prop(self, "height_max")
        layout.prop(self, "align_to_normal")
        layout.prop(self, "use_copy")
