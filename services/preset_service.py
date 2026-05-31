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
Preset service for managing user presets.
Provides functionality to save, load, export, and import presets.
"""

import json
import os
from typing import Dict, Optional
import bpy
from ..data.preset_schema import PresetSchema
from ..utils.logging import Logger


class PresetService:
    """Service for managing presets."""
    
    @staticmethod
    def get_preset_directory() -> str:
        """Get the directory where presets are stored."""
        # Use Blender's scripts directory
        scripts_dir = bpy.utils.user_resource('SCRIPTS')
        preset_dir = os.path.join(scripts_dir, 'presets', 'hardsurface')
        
        # Create directory if it doesn't exist
        if not os.path.exists(preset_dir):
            os.makedirs(preset_dir)
        
        return preset_dir
    
    @staticmethod
    def save_preset(
        name: str,
        operator_type: str,
        parameters: dict,
        description: str = ""
    ) -> bool:
        """Save a preset to the preset directory."""
        try:
            preset_dict = PresetSchema.create_preset_dict(
                name, operator_type, parameters, description
            )
            
            preset_dir = PresetService.get_preset_directory()
            filename = f"{name}.json"
            filepath = os.path.join(preset_dir, filename)
            
            with open(filepath, 'w') as f:
                json.dump(preset_dict, f, indent=2)
            
            Logger.info(f"Saved preset: {name}")
            return True
        except Exception as e:
            Logger.error(f"Failed to save preset: {e}")
            return False
    
    @staticmethod
    def load_preset(name: str) -> Optional[dict]:
        """Load a preset from the preset directory."""
        try:
            preset_dir = PresetService.get_preset_directory()
            filename = f"{name}.json"
            filepath = os.path.join(preset_dir, filename)
            
            if not os.path.exists(filepath):
                Logger.error(f"Preset not found: {name}")
                return None
            
            with open(filepath, 'r') as f:
                preset_dict = json.load(f)
            
            if not PresetSchema.validate_preset(preset_dict):
                Logger.error(f"Invalid preset format: {name}")
                return None
            
            Logger.info(f"Loaded preset: {name}")
            return preset_dict
        except Exception as e:
            Logger.error(f"Failed to load preset: {e}")
            return None
    
    @staticmethod
    def list_presets() -> list:
        """List all available presets."""
        try:
            preset_dir = PresetService.get_preset_directory()
            presets = []
            
            for filename in os.listdir(preset_dir):
                if filename.endswith('.json'):
                    preset_name = filename[:-5]  # Remove .json
                    presets.append(preset_name)
            
            return sorted(presets)
        except Exception as e:
            Logger.error(f"Failed to list presets: {e}")
            return []
    
    @staticmethod
    def delete_preset(name: str) -> bool:
        """Delete a preset."""
        try:
            preset_dir = PresetService.get_preset_directory()
            filename = f"{name}.json"
            filepath = os.path.join(preset_dir, filename)
            
            if os.path.exists(filepath):
                os.remove(filepath)
                Logger.info(f"Deleted preset: {name}")
                return True
            
            return False
        except Exception as e:
            Logger.error(f"Failed to delete preset: {e}")
            return False
    
    @staticmethod
    def export_preset(name: str, filepath: str) -> bool:
        """Export a preset to a specific filepath."""
        try:
            preset_dict = PresetService.load_preset(name)
            if preset_dict is None:
                return False
            
            with open(filepath, 'w') as f:
                json.dump(preset_dict, f, indent=2)
            
            Logger.info(f"Exported preset: {name} to {filepath}")
            return True
        except Exception as e:
            Logger.error(f"Failed to export preset: {e}")
            return False
    
    @staticmethod
    def import_preset(filepath: str) -> Optional[str]:
        """Import a preset from a specific filepath."""
        try:
            with open(filepath, 'r') as f:
                preset_dict = json.load(f)
            
            if not PresetSchema.validate_preset(preset_dict):
                Logger.error("Invalid preset format")
                return None
            
            name = preset_dict.get('name', 'imported_preset')
            
            # Save to preset directory
            if PresetService.save_preset(
                name,
                preset_dict['operator_type'],
                preset_dict['parameters'],
                preset_dict.get('description', '')
            ):
                Logger.info(f"Imported preset: {name}")
                return name
            
            return None
        except Exception as e:
            Logger.error(f"Failed to import preset: {e}")
            return None
