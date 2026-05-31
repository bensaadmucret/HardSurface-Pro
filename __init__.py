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
HardSurface Pro - Procedural Hard-Surface Generation Addon for Blender
"""

bl_info = {
    "name": "HardSurface Pro",
    "author": "Bensaad Mohammed",
    "version": (1, 0, 0),
    "blender": (3, 6, 0),
    "location": "View3D > Sidebar > HardSurface Pro",
    "description": "Procedural hard-surface generation addon for Blender. Random panels, extrude, scatter, and tubes.",
    "category": "Mesh",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "support": "COMMUNITY"
}

import bpy

# Import registration system
from .registration import classes, keymaps
from .properties import scene_props, operator_props


def register():
    """Register the addon."""
    # Register all Blender classes (Panels and Operators)
    classes.register()
    
    # Register property pointers on Scene and WindowManager
    scene_props.register()
    operator_props.register()
    
    # Register keymaps
    keymaps.register()
    
    print(f"HardSurface Pro {bl_info['version']} registered")


def unregister():
    """Unregister the addon."""
    # Unregister keymaps first
    keymaps.unregister()
    
    # Unregister property pointers
    operator_props.unregister()
    scene_props.unregister()
    
    # Unregister all classes last
    classes.unregister()
    
    print(f"HardSurface Pro {bl_info['version']} unregistered")
