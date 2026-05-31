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
Scene-level properties for the addon.
Stores global state for the active scene.
"""

import bpy
from bpy.props import IntProperty, StringProperty


class HardSurfaceSceneProps(bpy.types.PropertyGroup):
    """Global addon properties stored at scene level."""
    
    last_operator_seed: IntProperty(
        name="Last Seed",
        description="Seed used by the last operator for rebuild",
        default=0,
        min=0
    )
    
    last_operator_type: StringProperty(
        name="Last Operator",
        description="Type of the last operator executed",
        default=""
    )


def register():
    try:
        bpy.utils.register_class(HardSurfaceSceneProps)
    except ValueError:
        pass  # Already registered
        
    if not hasattr(bpy.types.Scene, 'hardsurface_props'):
        bpy.types.Scene.hardsurface_props = bpy.props.PointerProperty(
            type=HardSurfaceSceneProps
        )


def unregister():
    if hasattr(bpy.types.Scene, 'hardsurface_props'):
        del bpy.types.Scene.hardsurface_props
        
    try:
        bpy.utils.unregister_class(HardSurfaceSceneProps)
    except RuntimeError:
        pass  # Not registered
