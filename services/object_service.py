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
Object service for creating and managing Blender objects.
Provides utilities for object creation, collection management, and naming.
"""

import bpy
import bmesh
from typing import Optional


class ObjectService:
    """Service for managing Blender objects."""
    
    @staticmethod
    def create_mesh_object(name: str, mesh_data: Optional[bmesh.types.BMesh] = None) -> bpy.types.Object:
        """
        Create a new mesh object with optional bmesh data.
        """
        mesh = bpy.data.meshes.new(name)
        obj = bpy.data.objects.new(name, mesh)
        
        if mesh_data is not None:
            mesh_data.to_mesh(mesh)
        
        bpy.context.collection.objects.link(obj)
        return obj
    
    @staticmethod
    def duplicate_object(obj: bpy.types.Object, name_suffix: str = "_copy") -> bpy.types.Object:
        """
        Duplicate an object with a new name.
        """
        new_obj = obj.copy()
        new_obj.data = obj.data.copy()
        new_obj.name = f"{obj.name}{name_suffix}"
        bpy.context.collection.objects.link(new_obj)
        return new_obj
    
    @staticmethod
    def get_or_create_collection(name: str) -> bpy.types.Collection:
        """
        Get an existing collection or create a new one.
        """
        if name in bpy.data.collections:
            return bpy.data.collections[name]
        
        collection = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(collection)
        return collection
    
    @staticmethod
    def set_active_object(obj: bpy.types.Object):
        """Set an object as active in the current context."""
        bpy.context.view_layer.objects.active = obj
    
    @staticmethod
    def switch_to_edit_mode(obj: bpy.types.Object):
        """Switch object to Edit Mode."""
        ObjectService.set_active_object(obj)
        bpy.ops.object.mode_set(mode='EDIT')
    
    @staticmethod
    def switch_to_object_mode(obj: bpy.types.Object):
        """Switch object to Object Mode."""
        ObjectService.set_active_object(obj)
        bpy.ops.object.mode_set(mode='OBJECT')
