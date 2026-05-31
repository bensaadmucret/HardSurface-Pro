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
Preset schema definition.
Defines the structure of preset JSON files.
"""


class PresetSchema:
    """Schema for preset JSON files."""
    
    VERSION = "1.0"
    
    @staticmethod
    def create_preset_dict(
        name: str,
        operator_type: str,
        parameters: dict,
        description: str = ""
    ) -> dict:
        """Create a preset dictionary."""
        return {
            "version": PresetSchema.VERSION,
            "name": name,
            "operator_type": operator_type,
            "description": description,
            "parameters": parameters
        }
    
    @staticmethod
    def validate_preset(preset_dict: dict) -> bool:
        """Validate a preset dictionary."""
        required_keys = ["version", "name", "operator_type", "parameters"]
        return all(key in preset_dict for key in required_keys)
