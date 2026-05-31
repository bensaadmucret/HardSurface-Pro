# HardSurface Pro - Procedural Hard-Surface Generation Addon for Blender
# Copyright (C) 2024 HardSurface Pro Contributors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

"""
Displacement panel (Noise + Image) for the HardSurface addon.
"""

import bpy
from bpy.types import Panel


class VIEW3D_PT_hardsurface_displace(Panel):
    """Displacement panel using noise or image textures"""
    bl_label = "Displacement"
    bl_idname = "VIEW3D_PT_hardsurface_displace"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'HardSurface'
    bl_parent_id = 'VIEW3D_PT_hardsurface_main'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        wm = context.window_manager

        # Noise Displace section
        box = layout.box()
        box.label(text="Noise Displace", icon='MOD_NOISE')

        if hasattr(wm, 'noise_displace_props'):
            props = wm.noise_displace_props
            col = box.column(align=True)
            col.prop(props, "noise_type")
            col.prop(props, "seed")
            col.prop(props, "scale")
            col.prop(props, "strength")
            col.prop(props, "detail")
            col.prop(props, "use_normal")
            if not props.use_normal:
                col.prop(props, "axis")
            col.prop(props, "smooth")
            col.prop(props, "subdivide")

        box.operator("hardsurface.noise_displace", icon='PLAY')
        box.separator()

        # Image Displace section
        box = layout.box()
        box.label(text="Image Displace", icon='IMAGE_DATA')

        if hasattr(wm, 'image_displace_props'):
            props = wm.image_displace_props
            col = box.column(align=True)
            col.prop(props, "image_path")
            col.prop(props, "strength")
            col.prop(props, "use_normal")
            if not props.use_normal:
                col.prop(props, "axis")
            col.prop(props, "channel")
            col.prop(props, "use_uv")
            col.prop(props, "subdivide")

        box.operator("hardsurface.image_displace", icon='PLAY')
