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
Blender-specific utilities for context and operations.
Provides helpers for common Blender operations.
"""

import bpy
from typing import Optional


class BlenderUtils:
    """Utility class for Blender-specific operations."""
    
    @staticmethod
    def is_in_edit_mode() -> bool:
        """Check if the current context is in Edit Mode."""
        return bpy.context.mode == 'EDIT_MESH'
    
    @staticmethod
    def is_in_object_mode() -> bool:
        """Check if the current context is in Object Mode."""
        return bpy.context.mode == 'OBJECT'
    
    @staticmethod
    def get_context_area() -> Optional[bpy.types.Area]:
        """Get the current context area."""
        return bpy.context.area
    
    @staticmethod
    def get_context_region() -> Optional[bpy.types.Region]:
        """Get the current context region."""
        return bpy.context.region
    
    @staticmethod
    def force_update_mesh(obj: bpy.types.Object):
        """Force update of mesh data."""
        obj.data.update()
    
    @staticmethod
    def report_error(context, message: str):
        """Report an error to the user."""
        if context:
            context.report({'ERROR'}, message)
        else:
            print(f"ERROR: {message}")
    
    @staticmethod
    def report_info(context, message: str):
        """Report info to the user."""
        if context:
            context.report({'INFO'}, message)
        else:
            print(f"INFO: {message}")
    
    @staticmethod
    def report_warning(context, message: str):
        """Report a warning to the user."""
        if context:
            context.report({'WARNING'}, message)
        else:
            print(f"WARNING: {message}")
