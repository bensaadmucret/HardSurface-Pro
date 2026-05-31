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
Random Scatter generator.
Orchestrates the distribution of objects from a collection on a target surface.
"""

import bpy
import bmesh
from mathutils import Vector, Euler, Matrix
from typing import Tuple, List
from ..algorithms.randomization import Randomization
from ...services.selection_service import SelectionService
from ...services.object_service import ObjectService
from ...utils.bmesh_utils import BMeshUtils
from ...utils.logging import Logger


class ScatterGenerator:
    """Generator for scattering objects on mesh surfaces."""
    
    def __init__(self, seed: int):
        """Initialize generator with a seed."""
        self.seed = seed
        self.rng = Randomization(seed)
    
    def generate(
        self,
        target_obj: bpy.types.Object,
        collection_name: str,
        density: float,
        rotation_min: float,
        rotation_max: float,
        scale_min: float,
        scale_max: float,
        align_to_normal: bool,
        surface_offset: float
    ) -> Tuple[bool, str]:
        """
        Scatter objects from a collection on the target mesh.
        Returns (success, message).
        """
        # Validate collection
        if collection_name not in bpy.data.collections:
            return False, f"Collection '{collection_name}' not found"
        
        collection = bpy.data.collections[collection_name]
        source_objects = [obj for obj in collection.objects if obj.type == 'MESH']
        
        if not source_objects:
            return False, f"No mesh objects in collection '{collection_name}'"
        
        # Validate target
        is_valid, error = SelectionService.validate_mesh_object(target_obj)
        if not is_valid:
            return False, error
        
        Logger.info(f"Scattering {len(source_objects)} objects with seed {self.seed}")
        
        # Get target mesh data
        bm = bmesh.new()
        bm.from_mesh(target_obj.data)
        
        # Calculate surface area
        total_area = sum(face.calc_area() for face in bm.faces)
        if total_area == 0:
            bm.free()
            return False, "Target mesh has no surface area"
        
        # Calculate number of instances
        num_instances = int(total_area * density)
        if num_instances < 1:
            num_instances = 1
        
        # Get sample points on surface
        sample_points = self._sample_surface_points(bm, num_instances)
        bm.free()
        
        if not sample_points:
            return False, "Failed to sample surface points"
        
        # Create instances
        created_count = 0
        for point, normal in sample_points:
            # Select random object from collection
            source_obj = self.rng.random_choice(source_objects)
            
            # Calculate rotation
            if align_to_normal:
                # Align to normal with random rotation around normal
                rotation = self._calculate_aligned_rotation(normal, rotation_min, rotation_max)
            else:
                # Random rotation in all axes
                rotation = Euler((
                    self.rng.random_float(0, 360),
                    self.rng.random_float(0, 360),
                    self.rng.random_float(0, 360)
                ), 'XYZ')
            
            # Calculate scale
            scale = self.rng.random_float(scale_min, scale_max)
            scale_vec = Vector((scale, scale, scale))
            
            # Calculate position with offset
            position = point + normal * surface_offset
            
            # Create instance
            new_obj = self._create_instance(source_obj, position, rotation, scale_vec)
            if new_obj:
                created_count += 1
        
        Logger.info(f"Created {created_count} scattered instances")
        return True, f"Created {created_count} scattered instances"
    
    def _sample_surface_points(self, bm: bmesh.types.BMesh, count: int) -> List[Tuple[Vector, Vector]]:
        """Sample random points on mesh surface with normals."""
        points = []
        
        # Weight faces by area
        face_areas = [face.calc_area() for face in bm.faces]
        total_area = sum(face_areas)
        
        for _ in range(count):
            # Select random face weighted by area
            r = self.rng.random_float(0, total_area)
            cumulative = 0
            selected_face = None
            
            for face, area in zip(bm.faces, face_areas):
                cumulative += area
                if r <= cumulative:
                    selected_face = face
                    break
            
            if selected_face is None:
                selected_face = bm.faces[-1]
            
            # Sample random point on face
            point = self._sample_point_on_face(selected_face)
            normal = selected_face.normal.copy()
            points.append((point, normal))
        
        return points
    
    def _sample_point_on_face(self, face: bmesh.types.BMFace) -> Vector:
        """Sample a random point on a face using barycentric coordinates."""
        verts = list(face.verts)
        if len(verts) < 3:
            return face.calc_center_median()
        
        # Triangulate the face if it has more than 3 vertices
        if len(verts) > 3:
            # Use the first triangle of the face
            v0 = verts[0].co
            v1 = verts[1].co
            v2 = verts[2].co
        else:
            v0 = verts[0].co
            v1 = verts[1].co
            v2 = verts[2].co
        
        # Generate random barycentric coordinates
        r1 = self.rng.random_float(0, 1)
        r2 = self.rng.random_float(0, 1)
        
        # Ensure point is inside triangle
        if r1 + r2 > 1:
            r1 = 1 - r1
            r2 = 1 - r2
        
        # Calculate point using barycentric coordinates
        point = v0 + (v1 - v0) * r1 + (v2 - v0) * r2
        return point
    
    def _calculate_aligned_rotation(self, normal: Vector, rot_min: float, rot_max: float) -> Euler:
        """Calculate rotation aligned to surface normal with random twist."""
        from mathutils import Vector
        
        # Create rotation matrix that aligns Z axis to normal
        z_axis = Vector((0, 0, 1))
        if normal.cross(z_axis).length < 0.001:
            # Normal is parallel to Z axis
            if normal.dot(z_axis) > 0:
                rotation_matrix = Matrix.Identity(3)
            else:
                rotation_matrix = Matrix.Rotation(180, 3, 'X')
        else:
            rotation_matrix = normal.to_track_quat('Z', 'Y').to_matrix()
        
        # Add random rotation around normal (Z axis)
        twist = self.rng.random_float(rot_min, rot_max)
        twist_matrix = Matrix.Rotation(twist, 3, 'Z')
        
        final_matrix = rotation_matrix @ twist_matrix
        return final_matrix.to_euler()
    
    def _create_instance(
        self,
        source_obj: bpy.types.Object,
        position: Vector,
        rotation: Euler,
        scale: Vector
    ) -> bpy.types.Object:
        """Create an instance of the source object with given transform."""
        # Duplicate the object
        new_obj = source_obj.copy()
        new_obj.data = source_obj.data.copy()
        new_obj.name = f"{source_obj.name}_scatter"
        
        # Set transform
        new_obj.location = position
        new_obj.rotation_euler = rotation
        new_obj.scale = scale
        
        # Link to scene
        bpy.context.collection.objects.link(new_obj)
        
        return new_obj
    
    def get_config_dict(self) -> dict:
        """Get current configuration as dictionary for presets."""
        return {
            'seed': self.seed,
            'type': 'random_scatter'
        }
