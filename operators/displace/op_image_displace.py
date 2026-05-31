# HardSurface Pro - Procedural Hard-Surface Generation Addon for Blender
# Copyright (C) 2024 HardSurface Pro Contributors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

"""
Image Displace operator.
Displaces selected vertices using an image texture as a height map.
"""

import bpy
import bmesh
from mathutils import Vector
from bpy.types import Operator
from bpy.props import FloatProperty, BoolProperty, EnumProperty, StringProperty
from ...utils.blender_utils import BlenderUtils


class OBJECT_OT_image_displace(Operator):
    """Displace selected geometry using an image texture as height map"""
    bl_idname = "hardsurface.image_displace"
    bl_label = "Image Displace"
    bl_description = "Displace selected vertices using an image texture"
    bl_options = {'REGISTER', 'UNDO'}

    image_path: StringProperty(
        name="Image",
        description="Path to the image texture to use as height map",
        default="",
        subtype='FILE_PATH'
    )

    strength: FloatProperty(
        name="Strength",
        description="Displacement strength",
        default=1.0,
        min=-10.0,
        max=10.0
    )

    use_normal: BoolProperty(
        name="Along Normal",
        description="Displace along vertex normals",
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

    channel: EnumProperty(
        name="Channel",
        description="Image channel to use as height",
        items=[
            ('LUMINANCE', "Luminance", "Grayscale luminance"),
            ('RED', "Red", "Red channel"),
            ('GREEN', "Green", "Green channel"),
            ('BLUE', "Blue", "Blue channel"),
            ('ALPHA', "Alpha", "Alpha channel"),
        ],
        default='LUMINANCE'
    )

    use_uv: BoolProperty(
        name="Use UV",
        description="Map image using active UV map instead of planar projection",
        default=True
    )

    subdivide: bpy.props.IntProperty(
        name="Subdivide",
        description="Subdivide selected faces before displacement (0 = none)",
        default=2,
        min=0,
        max=6
    )

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj and obj.type == 'MESH' and obj.mode == 'EDIT'

    def invoke(self, context, event):
        wm = context.window_manager
        if hasattr(wm, 'image_displace_props'):
            props = wm.image_displace_props
            self.image_path = props.image_path
            self.strength = props.strength
            self.use_normal = props.use_normal
            self.axis = props.axis
            self.channel = props.channel
            self.use_uv = props.use_uv
            self.subdivide = props.subdivide
        return self.execute(context)

    def execute(self, context):
        obj = context.active_object
        mesh = obj.data

        if not self.image_path:
            BlenderUtils.report_error(self, "No image selected")
            return {'CANCELLED'}

        # Load image if needed
        img_name = bpy.path.basename(self.image_path)
        image = bpy.data.images.get(img_name)
        if image is None:
            try:
                image = bpy.data.images.load(self.image_path, check_existing=True)
            except RuntimeError:
                BlenderUtils.report_error(self, f"Could not load image: {self.image_path}")
                return {'CANCELLED'}

        if image is None or len(image.pixels) == 0:
            BlenderUtils.report_error(self, "Image has no pixels")
            return {'CANCELLED'}

        # Auto-subdivide using native operator (keeps selection)
        if self.subdivide > 0:
            for _ in range(self.subdivide):
                bpy.ops.mesh.subdivide(number_cuts=1, smoothness=0)

        bm = bmesh.from_edit_mesh(mesh)
        bm.verts.ensure_lookup_table()

        selected_verts = [v for v in bm.verts if v.select]
        if not selected_verts:
            BlenderUtils.report_error(self, "No vertices selected")
            return {'CANCELLED'}

        width, height = image.size
        pixels = image.pixels

        def sample_image(uvx, uvy):
            """Bilinear sample of image at UV coordinates (0..1)."""
            # Clamp/wrap UVs to 0..1
            uvx = uvx % 1.0
            uvy = uvy % 1.0
            if uvx < 0:
                uvx += 1.0
            if uvy < 0:
                uvy += 1.0

            x = uvx * (width - 1)
            y = uvy * (height - 1)
            ix = int(x)
            iy = int(y)
            fx = x - ix
            fy = y - iy

            # Clamp to image bounds
            ix = max(0, min(ix, width - 1))
            iy = max(0, min(iy, height - 1))
            ix2 = min(ix + 1, width - 1)
            iy2 = min(iy + 1, height - 1)

            def get_pixel(px, py):
                idx = (py * width + px) * 4
                r = pixels[idx]
                g = pixels[idx + 1]
                b = pixels[idx + 2]
                a = pixels[idx + 3]
                if self.channel == 'LUMINANCE':
                    return 0.299 * r + 0.587 * g + 0.114 * b
                elif self.channel == 'RED':
                    return r
                elif self.channel == 'GREEN':
                    return g
                elif self.channel == 'BLUE':
                    return b
                elif self.channel == 'ALPHA':
                    return a
                return 0.0

            v00 = get_pixel(ix, iy)
            v10 = get_pixel(ix2, iy)
            v01 = get_pixel(ix, iy2)
            v11 = get_pixel(ix2, iy2)

            # Bilinear interpolation
            v0 = v00 * (1 - fx) + v10 * fx
            v1 = v01 * (1 - fx) + v11 * fx
            return v0 * (1 - fy) + v1 * fy

        # Active UV layer
        uv_layer = bm.loops.layers.uv.active

        for v in selected_verts:
            # Determine UV / planar coordinate
            if self.use_uv and uv_layer:
                # Average UVs of connected loops for this vertex
                uvs = [l[uv_layer].uv for l in v.link_loops]
                avg_uv = sum((Vector(uv) for uv in uvs), Vector((0.0, 0.0))) / len(uvs)
                uvx, uvy = avg_uv.x, avg_uv.y
            else:
                # Planar projection from local XY
                uvx = v.co.x
                uvy = v.co.y

            h = sample_image(uvx, uvy)
            offset = (h - 0.5) * self.strength * 2.0  # Center around 0

            if self.use_normal:
                # Use face normals for cleaner displacement on sharp edges
                linked_faces = [f for f in v.link_faces if f.select]
                if linked_faces:
                    no = sum((f.normal for f in linked_faces), Vector((0.0, 0.0, 0.0))).normalized()
                else:
                    no = v.normal.normalized()
                v.co += no * offset
            else:
                axis_vec = Vector((0.0, 0.0, 0.0))
                if self.axis == 'X':
                    axis_vec.x = 1.0
                elif self.axis == 'Y':
                    axis_vec.y = 1.0
                else:
                    axis_vec.z = 1.0
                v.co += axis_vec * offset

        bmesh.update_edit_mesh(mesh, loop_triangles=True)
        BlenderUtils.report_info(self, f"Image Displace applied to {len(selected_verts)} vertices")

        # Save props
        wm = context.window_manager
        if hasattr(wm, 'image_displace_props'):
            props = wm.image_displace_props
            props.image_path = self.image_path
            props.strength = self.strength
            props.use_normal = self.use_normal
            props.axis = self.axis
            props.channel = self.channel
            props.use_uv = self.use_uv
            props.subdivide = self.subdivide

        return {'FINISHED'}
