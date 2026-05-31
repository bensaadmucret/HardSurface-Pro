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
Flanges/Couplings generator.
Creates flange meshes along curves.
"""

import bpy
from mathutils import Vector, Matrix
from typing import Tuple
from ..algorithms.randomization import Randomization
from ...utils.logging import Logger


class FlangesGenerator:
    """Generator for flange couplings along curves."""
    
    def __init__(self, seed: int):
        self.seed = seed
        self.rng = Randomization(seed)
    
    def generate(
        self,
        curve_obj: bpy.types.Object,
        flange_size: float,
        flange_depth: float,
        spacing: float,
        probability: float,
        use_existing_curve: bool
    ) -> Tuple[bool, str]:
        """
        Generate flanges along a curve.
        Returns (success, message).
        """
        if curve_obj.type != 'CURVE':
            return False, "Selected object is not a curve"
        
        Logger.info(f"Generating flanges on curve {curve_obj.name}")
        
        flanges_created = 0
        curve = curve_obj.data
        
        for spline in curve.splines:
            if spline.type == 'NURBS' or spline.type == 'POLY':
                points = spline.points
            elif spline.type == 'BEZIER':
                points = spline.bezier_points
            else:
                continue
            
            for i in range(len(points)):
                if i % max(1, int(spacing * 2)) != 0:
                    continue
                if not self.rng.random_bool(probability):
                    continue
                
                point = points[i]
                if spline.type == 'BEZIER':
                    location = point.co
                    tangent = point.handle_right - point.co
                else:
                    location = Vector(point.co[:3])
                    tangent = Vector((0, 0, 1))
                
                if tangent.length > 0:
                    tangent.normalize()
                
                self._create_flange(location, tangent, flange_size, flange_depth, flanges_created)
                flanges_created += 1
        
        return True, f"Created {flanges_created} flanges"
    
    def _create_flange(
        self,
        location: Vector,
        normal: Vector,
        size: float,
        depth: float,
        index: int
    ):
        """Create a cylindrical flange mesh."""
        bpy.ops.mesh.primitive_cylinder_add(
            radius=size,
            depth=depth,
            location=location
        )
        flange = bpy.context.active_object
        flange.name = f"Flange_{index}"
        
        if normal.length > 0:
            up = Vector((0, 0, 1))
            if abs(normal.dot(up)) > 0.99:
                up = Vector((1, 0, 0))
            
            rot_matrix = normal.to_track_quat('Z', 'Y').to_matrix().to_4x4()
            flange.matrix_world = rot_matrix @ flange.matrix_world
