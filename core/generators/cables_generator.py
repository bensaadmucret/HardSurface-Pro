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
Random Cables generator.
Creates catenary or bezier curves as hanging cables.
"""

import bpy
import math
from mathutils import Vector
from typing import Tuple
from ..algorithms.randomization import Randomization
from ...utils.logging import Logger


class CablesGenerator:
    """Generator for random hanging cables."""
    
    def __init__(self, seed: int):
        self.seed = seed
        self.rng = Randomization(seed)
    
    def generate(
        self,
        obj: bpy.types.Object,
        cable_type: str,
        count: int,
        radius: float,
        slack: float,
        resolution: int,
        length_min: float,
        length_max: float
    ) -> Tuple[bool, str]:
        """
        Generate random cables.
        Returns (success, message).
        """
        Logger.info(f"Generating {count} cables of type {cable_type}")
        
        cables_created = 0
        for i in range(count):
            length = self.rng.random_float(length_min, length_max)
            
            if cable_type == 'CATENARY':
                self._create_catenary_cable(obj, length, slack, resolution, radius, i)
            elif cable_type == 'BEZIER':
                self._create_bezier_cable(obj, length, resolution, radius, i)
            else:
                self._create_straight_cable(obj, length, radius, i)
            
            cables_created += 1
        
        return True, f"Created {cables_created} cables"
    
    def _create_catenary_cable(
        self,
        obj: bpy.types.Object,
        length: float,
        slack: float,
        resolution: int,
        radius: float,
        index: int
    ):
        """Create a catenary (hanging) cable curve."""
        start = Vector((
            self.rng.random_float(-1, 1),
            self.rng.random_float(-1, 1),
            self.rng.random_float(0, 1)
        ))
        end = start + Vector((length, 0, 0))
        
        curve_data = bpy.data.curves.new(f"Cable_{index}", type='CURVE')
        curve_data.dimensions = '3D'
        curve_data.resolution_u = resolution
        curve_data.bevel_depth = radius
        
        spline = curve_data.splines.new('NURBS')
        spline.points.add(resolution - 1)
        
        for i in range(resolution):
            t = i / (resolution - 1)
            x = start.x + (end.x - start.x) * t
            z = start.z + (end.z - start.z) * t - slack * (1 - 4 * (t - 0.5) ** 2)
            y = start.y + (end.y - start.y) * t
            spline.points[i].co = (x, y, z, 1)
        
        curve_obj = bpy.data.objects.new(f"Cable_{index}", curve_data)
        bpy.context.collection.objects.link(curve_obj)
    
    def _create_bezier_cable(
        self,
        obj: bpy.types.Object,
        length: float,
        resolution: int,
        radius: float,
        index: int
    ):
        """Create a bezier cable curve."""
        curve_data = bpy.data.curves.new(f"BezierCable_{index}", type='CURVE')
        curve_data.dimensions = '3D'
        curve_data.resolution_u = resolution
        curve_data.bevel_depth = radius
        
        spline = curve_data.splines.new('BEZIER')
        spline.bezier_points.add(2)
        
        p0 = Vector((0, 0, 0))
        p1 = Vector((length * 0.3, 0, self.rng.random_float(-0.5, 0.5)))
        p2 = Vector((length * 0.7, 0, self.rng.random_float(-0.5, 0.5)))
        p3 = Vector((length, 0, 0))
        
        for i, p in enumerate([p0, p1, p2, p3]):
            spline.bezier_points[i].co = p
        
        curve_obj = bpy.data.objects.new(f"BezierCable_{index}", curve_data)
        bpy.context.collection.objects.link(curve_obj)
    
    def _create_straight_cable(
        self,
        obj: bpy.types.Object,
        length: float,
        radius: float,
        index: int
    ):
        """Create a straight cable."""
        curve_data = bpy.data.curves.new(f"StraightCable_{index}", type='CURVE')
        curve_data.dimensions = '3D'
        curve_data.bevel_depth = radius
        
        spline = curve_data.splines.new('POLY')
        spline.points.add(1)
        spline.points[0].co = (0, 0, 0, 1)
        spline.points[1].co = (length, 0, 0, 1)
        
        curve_obj = bpy.data.objects.new(f"StraightCable_{index}", curve_data)
        bpy.context.collection.objects.link(curve_obj)
