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
BMesh utilities for common mesh operations.
Provides wrappers and helpers for bmesh operations.
"""

import bmesh
from typing import List, Optional
import bpy


class BMeshUtils:
    """Utility class for bmesh operations."""
    
    @staticmethod
    def get_edit_bmesh(obj: bpy.types.Object) -> Optional[bmesh.types.BMesh]:
        """
        Get the bmesh for an object in Edit Mode.
        Returns None if not in Edit Mode.
        """
        if obj.mode != 'EDIT':
            return None
        return bmesh.from_edit_mesh(obj.data)
    
    @staticmethod
    def get_object_bmesh(obj: bpy.types.Object) -> bmesh.types.BMesh:
        """
        Get a new bmesh from an object in Object Mode.
        """
        bm = bmesh.new()
        bm.from_mesh(obj.data)
        return bm
    
    @staticmethod
    def apply_to_object(bm: bmesh.types.BMesh, obj: bpy.types.Object):
        """
        Apply bmesh changes to an object.
        """
        if obj.mode == 'EDIT':
            bmesh.update_edit_mesh(obj.data)
        else:
            bm.to_mesh(obj.data)
            bm.free()
    
    @staticmethod
    def inset_face(bm: bmesh.types.BMesh, face: bmesh.types.BMFace, 
                   amount: float, use_even_offset: bool = False) -> Optional[bmesh.types.BMFace]:
        """
        Inset a single face by a given amount.
        Returns the new inset face or None if failed.
        """
        geom = [face]
        result = bmesh.ops.inset_individual(
            bm,
            faces=geom,
            thickness=amount,
            use_even_offset=use_even_offset
        )
        
        # Find the new face (the one that was created)
        if result.get('faces'):
            return result['faces'][0]
        return None
    
    @staticmethod
    def extrude_face(bm: bmesh.types.BMesh, face: bmesh.types.BMFace, 
                     depth: float) -> Optional[bmesh.types.BMFace]:
        """
        Extrude a single face by a given depth along its normal.
        Returns the new extruded face or None if failed.
        """
        geom = [face]
        result = bmesh.ops.extrude_face_region(bm, geom=geom)
        
        if result.get('faces'):
            # Move the new faces along the normal
            new_faces = result['faces']
            normal = face.normal.copy()
            bmesh.ops.translate(bm, vec=normal * depth, verts=result['verts'])
            return new_faces[0] if new_faces else None
        return None
    
    @staticmethod
    def get_face_center(face: bmesh.types.BMFace) -> tuple:
        """Get the center point of a face."""
        return face.calc_center_median()
    
    @staticmethod
    def get_face_normal(face: bmesh.types.BMFace) -> tuple:
        """Get the normal vector of a face."""
        return face.normal.copy()
