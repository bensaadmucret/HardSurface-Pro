# HardSurface Pro - Procedural Hard-Surface Generation Addon for Blender
# Copyright (C) 2024 HardSurface Pro Contributors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

"""
Noise Displace operator.
Displaces selected vertices using Blender's procedural noise functions.
"""

import bpy
import bmesh
import mathutils
from mathutils import Vector
from bpy.types import Operator
from bpy.props import FloatProperty, IntProperty, BoolProperty, EnumProperty
from ...services.selection_service import SelectionService
from ...utils.blender_utils import BlenderUtils


class OBJECT_OT_noise_displace(Operator):
    """Displace selected geometry using procedural noise"""
    bl_idname = "hardsurface.noise_displace"
    bl_label = "Noise Displace"
    bl_description = "Displace selected vertices using procedural noise"
    bl_options = {'REGISTER', 'UNDO'}

    noise_type: EnumProperty(
        name="Noise Type",
        description="Type of procedural noise to use",
        items=[
            ('PERLIN', "Perlin", "Classic Perlin noise"),
            ('VORONOI_F1', "Voronoi F1", "Voronoi distance to nearest cell center"),
            ('VORONOI_F2', "Voronoi F2", "Voronoi distance to 2nd nearest cell center"),
            ('VORONOI_F2F1', "Voronoi F2-F1", "Difference between F2 and F1"),
            ('CELLNOISE', "Cell Noise", "Cell-based noise"),
            ('SIMPLEX', "Simplex", "Simplex noise"),
        ],
        default='PERLIN'
    )

    seed: IntProperty(
        name="Seed",
        description="Noise seed for reproducible results",
        default=0,
        min=0,
        max=2147483647
    )

    scale: FloatProperty(
        name="Scale",
        description="Scale of the noise (lower = larger features)",
        default=2.0,
        min=0.001,
        max=100.0
    )

    strength: FloatProperty(
        name="Strength",
        description="Displacement strength",
        default=0.5,
        min=0.0,
        max=10.0
    )

    detail: FloatProperty(
        name="Detail",
        description="Noise detail / octaves",
        default=2.0,
        min=0.0,
        max=16.0
    )

    use_normal: BoolProperty(
        name="Along Normal",
        description="Displace along vertex normals instead of Z axis",
        default=True
    )

    axis: EnumProperty(
        name="Axis",
        description="Displacement axis when not using normals",
        items=[
            ('X', "X", "Local X axis"),
            ('Y', "Y", "Local Y axis"),
            ('Z', "Z", "Local Z axis"),
        ],
        default='Z'
    )

    smooth: BoolProperty(
        name="Smooth",
        description="Use smooth interpolation",
        default=True
    )

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj and obj.type == 'MESH' and obj.mode == 'EDIT'

    def invoke(self, context, event):
        wm = context.window_manager
        if hasattr(wm, 'noise_displace_props'):
            props = wm.noise_displace_props
            self.seed = props.seed
            self.scale = props.scale
            self.strength = props.strength
            self.detail = props.detail
            self.noise_type = props.noise_type
            self.use_normal = props.use_normal
            self.axis = props.axis
            self.smooth = props.smooth
        return self.execute(context)

    def execute(self, context):
        obj = context.active_object
        mesh = obj.data

        # Validate
        if obj.mode != 'EDIT':
            BlenderUtils.report_error(self, "Must be in Edit Mode")
            return {'CANCELLED'}

        bm = bmesh.from_edit_mesh(mesh)
        bm.verts.ensure_lookup_table()

        # Get selected vertices
        selected_verts = [v for v in bm.verts if v.select]
        if not selected_verts:
            BlenderUtils.report_error(self, "No vertices selected")
            return {'CANCELLED'}

        # Seed offset
        mathutils.noise.seed_set(self.seed)

        # Map noise type string to mathutils.noise type constant
        noise_map = {
            'PERLIN': mathutils.noise.types.PERLIN_ORIGINAL,
            'VORONOI_F1': mathutils.noise.types.VORONOI_F1,
            'VORONOI_F2': mathutils.noise.types.VORONOI_F2,
            'VORONOI_F2F1': mathutils.noise.types.VORONOI_F2F1,
            'CELLNOISE': mathutils.noise.types.CELLNOISE,
            'SIMPLEX': mathutils.noise.types.SIMPLEX,
        }
        basis = noise_map.get(self.noise_type, mathutils.noise.types.PERLIN_ORIGINAL)

        for v in selected_verts:
            co = obj.matrix_world @ v.co
            # Sample noise at vertex position scaled by scale
            nval = mathutils.noise.noise(
                co * self.scale,
                noise_basis=basis
            )

            # Optionally add turbulence for detail
            if self.detail > 0:
                nval += mathutils.noise.turbulence(
                    co * self.scale,
                    self.detail,
                    False,  # hard (False = smooth)
                    noise_basis=basis
                ) * 0.3

            # Normalize roughly to 0..1 or -1..1 depending on noise
            offset = nval * self.strength

            if self.use_normal:
                # Transform normal to world space for displacement
                no = (obj.matrix_world.to_3x3() @ v.normal).normalized()
                v.co += no * offset
            else:
                # Use local axis
                axis_vec = Vector((0.0, 0.0, 0.0))
                if self.axis == 'X':
                    axis_vec.x = 1.0
                elif self.axis == 'Y':
                    axis_vec.y = 1.0
                else:
                    axis_vec.z = 1.0
                v.co += axis_vec * offset

        bmesh.update_edit_mesh(mesh, loop_triangles=True)
        BlenderUtils.report_info(self, f"Noise Displace applied to {len(selected_verts)} vertices")

        # Save props
        wm = context.window_manager
        if hasattr(wm, 'noise_displace_props'):
            props = wm.noise_displace_props
            props.seed = self.seed
            props.scale = self.scale
            props.strength = self.strength
            props.detail = self.detail
            props.noise_type = self.noise_type
            props.use_normal = self.use_normal
            props.axis = self.axis
            props.smooth = self.smooth

        return {'FINISHED'}
