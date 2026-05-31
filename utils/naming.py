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
Naming utilities for generated objects.
Provides consistent naming conventions for addon-generated objects.
"""


class NamingUtils:
    """Utility class for naming conventions."""
    
    PREFIX_PANELS = "HS_Panels"
    PREFIX_EXTRUDE = "HS_Extrude"
    PREFIX_SCATTER = "HS_Scatter"
    PREFIX_TUBES = "HS_Tubes"
    
    @staticmethod
    def generate_name(prefix: str, base_name: str = None) -> str:
        """
        Generate a name with prefix and optional base name.
        """
        if base_name:
            return f"{prefix}_{base_name}"
        return prefix
    
    @staticmethod
    def get_unique_name(prefix: str, base_name: str = None) -> str:
        """
        Generate a unique name that doesn't conflict with existing objects.
        """
        import bpy
        
        base = NamingUtils.generate_name(prefix, base_name)
        if base not in bpy.data.objects:
            return base
        
        counter = 1
        while f"{base}.{counter:03d}" in bpy.data.objects:
            counter += 1
        
        return f"{base}.{counter:03d}"
