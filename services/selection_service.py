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
Selection service for reading and preparing Blender selections.
Provides utilities to extract selected faces, edges, and objects.
"""

import bpy
import bmesh
from typing import List, Tuple, Optional
from .object_service import ObjectService


class SelectionService:
    """Service for managing Blender selections."""
    
    @staticmethod
    def get_active_object() -> Optional[bpy.types.Object]:
        """Get the active object in the current context."""
        return bpy.context.active_object
    
    @staticmethod
    def get_selected_objects() -> List[bpy.types.Object]:
        """Get all selected objects in the current context."""
        return bpy.context.selected_objects
    
    @staticmethod
    def get_selected_faces(obj: bpy.types.Object) -> List[int]:
        """
        Get indices of selected faces in Edit Mode.
        Returns empty list if not in Edit Mode or no faces selected.
        """
        if obj.mode != 'EDIT':
            return []
        
        bm = bmesh.from_edit_mesh(obj.data)
        face_indices = [face.index for face in bm.faces if face.select]
        return face_indices
    
    @staticmethod
    def get_selected_edges(obj: bpy.types.Object) -> List[int]:
        """
        Get indices of selected edges in Edit Mode.
        Returns empty list if not in Edit Mode or no edges selected.
        """
        if obj.mode != 'EDIT':
            return []
        
        bm = bmesh.from_edit_mesh(obj.data)
        edge_indices = [edge.index for edge in bm.edges if edge.select]
        return edge_indices
    
    @staticmethod
    def validate_mesh_object(obj: bpy.types.Object) -> Tuple[bool, str]:
        """
        Validate that an object is a valid mesh for operations.
        Returns (is_valid, error_message).
        """
        if obj is None:
            return False, "No active object selected"
        
        if obj.type != 'MESH':
            return False, f"Object '{obj.name}' is not a mesh"
        
        return True, ""
    
    @staticmethod
    def validate_face_selection(obj: bpy.types.Object) -> Tuple[bool, str]:
        """
        Validate that there are selected faces for operations.
        Returns (is_valid, error_message).
        """
        is_valid, error = SelectionService.validate_mesh_object(obj)
        if not is_valid:
            return is_valid, error
        
        if obj.mode != 'EDIT':
            return False, "Object must be in Edit Mode with faces selected"
        
        selected_faces = SelectionService.get_selected_faces(obj)
        if not selected_faces:
            return False, "No faces selected"
        
        return True, ""
