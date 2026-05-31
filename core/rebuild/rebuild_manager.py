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
Rebuild manager for reapplying last operator with same parameters.
Provides functionality to regenerate results with stored seed and parameters.
"""

import bpy
from typing import Optional, Tuple
from ...services.selection_service import SelectionService
from ...utils.blender_utils import BlenderUtils
from ...utils.logging import Logger


class RebuildManager:
    """Manager for rebuilding last operation."""
    
    @staticmethod
    def can_rebuild(context) -> bool:
        """Check if rebuild is possible."""
        if not hasattr(context.scene, 'hardsurface_props'):
            return False
        
        props = context.scene.hardsurface_props
        return bool(props.last_operator_type)
    
    @staticmethod
    def get_last_operator_info(context) -> Tuple[Optional[str], Optional[int]]:
        """Get last operator type and seed."""
        if not hasattr(context.scene, 'hardsurface_props'):
            return None, None
        
        props = context.scene.hardsurface_props
        return props.last_operator_type, props.last_operator_seed
    
    @staticmethod
    def rebuild(context) -> Tuple[bool, str]:
        """
        Rebuild the last operation with stored parameters.
        Returns (success, message).
        """
        operator_type, seed = RebuildManager.get_last_operator_info(context)
        
        if operator_type is None:
            return False, "No previous operation to rebuild"
        
        obj = context.active_object
        
        # Validate selection based on operator type
        if operator_type in ["random_panels", "random_extrude"]:
            is_valid, error = SelectionService.validate_face_selection(obj)
            if not is_valid:
                return False, error
        elif operator_type == "random_tubes":
            is_valid, error = SelectionService.validate_mesh_object(obj)
            if not is_valid:
                return False, error
            if obj.mode != 'EDIT':
                return False, "Object must be in Edit Mode with edges selected"
        elif operator_type in ["random_loop_extrude", "panel_screws", "random_axis_extrude", "random_cells"]:
            is_valid, error = SelectionService.validate_face_selection(obj)
            if not is_valid:
                return False, error
        elif operator_type in ["random_cables", "flanges"]:
            if obj is None or obj.type != 'CURVE':
                return False, "Select a curve object"
        elif operator_type == "random_scatter":
            is_valid, error = SelectionService.validate_mesh_object(obj)
            if not is_valid:
                return False, error
        
        Logger.info(f"Rebuilding {operator_type} with seed {seed}")
        
        # Call the appropriate operator
        if operator_type == "random_panels":
            wm = context.window_manager
            if hasattr(wm, 'random_panels_props'):
                props = wm.random_panels_props
                bpy.ops.mesh.random_panels(
                    seed=seed,
                    probability=props.probability,
                    inset_min=props.inset_min,
                    inset_max=props.inset_max,
                    depth_min=props.depth_min,
                    depth_max=props.depth_max,
                    safety_margin=props.safety_margin,
                    use_copy=props.use_copy
                )
                return True, f"Rebuilt {operator_type}"
        
        elif operator_type == "random_extrude":
            wm = context.window_manager
            if hasattr(wm, 'random_extrude_props'):
                props = wm.random_extrude_props
                bpy.ops.mesh.random_extrude(
                    seed=seed,
                    extrude_rate=props.extrude_rate,
                    height_min=props.height_min,
                    height_max=props.height_max,
                    taper_min=props.taper_min,
                    taper_max=props.taper_max,
                    max_faces=props.max_faces,
                    group_islands=props.group_islands
                )
                return True, f"Rebuilt {operator_type}"
        
        elif operator_type == "random_scatter":
            wm = context.window_manager
            if hasattr(wm, 'random_scatter_props'):
                props = wm.random_scatter_props
                bpy.ops.mesh.random_scatter(
                    seed=seed,
                    collection_name=props.collection_name,
                    density=props.density,
                    rotation_min=props.rotation_min,
                    rotation_max=props.rotation_max,
                    scale_min=props.scale_min,
                    scale_max=props.scale_max,
                    align_to_normal=props.align_to_normal,
                    surface_offset=props.surface_offset
                )
                return True, f"Rebuilt {operator_type}"
        
        elif operator_type == "random_tubes":
            wm = context.window_manager
            if hasattr(wm, 'random_tubes_props'):
                props = wm.random_tubes_props
                bpy.ops.mesh.random_tubes(
                    seed=seed,
                    radius=props.radius,
                    radius_variation=props.radius_variation,
                    segments=props.segments,
                    smooth=props.smooth
                )
                return True, f"Rebuilt {operator_type}"
        
        elif operator_type == "random_loop_extrude":
            wm = context.window_manager
            if hasattr(wm, 'random_loop_extrude_props'):
                props = wm.random_loop_extrude_props
                bpy.ops.mesh.random_loop_extrude(
                    seed=seed,
                    iterations=props.iterations,
                    probability=props.probability,
                    height_min=props.height_min,
                    height_max=props.height_max,
                    height_decay=props.height_decay,
                    inset_min=props.inset_min,
                    inset_max=props.inset_max,
                    taper=props.taper,
                    use_copy=props.use_copy
                )
                return True, f"Rebuilt {operator_type}"
        
        elif operator_type == "panel_screws":
            wm = context.window_manager
            if hasattr(wm, 'panel_screws_props'):
                props = wm.panel_screws_props
                bpy.ops.mesh.panel_screws(
                    seed=seed,
                    screw_size=props.screw_size,
                    screw_depth=props.screw_depth,
                    probability=props.probability,
                    screw_type=props.screw_type
                )
                return True, f"Rebuilt {operator_type}"
        
        elif operator_type == "random_axis_extrude":
            wm = context.window_manager
            if hasattr(wm, 'random_axis_extrude_props'):
                props = wm.random_axis_extrude_props
                bpy.ops.mesh.random_axis_extrude(
                    seed=seed,
                    iterations=props.iterations,
                    probability_x=props.probability_x,
                    probability_y=props.probability_y,
                    probability_z=props.probability_z,
                    length_min=props.length_min,
                    length_max=props.length_max,
                    scale_decay=props.scale_decay,
                    use_copy=props.use_copy
                )
                return True, f"Rebuilt {operator_type}"
        
        elif operator_type == "random_cells":
            wm = context.window_manager
            if hasattr(wm, 'random_cells_props'):
                props = wm.random_cells_props
                bpy.ops.mesh.random_cells(
                    seed=seed,
                    cell_type=props.cell_type,
                    density=props.density,
                    size_min=props.size_min,
                    size_max=props.size_max,
                    height_min=props.height_min,
                    height_max=props.height_max,
                    align_to_normal=props.align_to_normal,
                    use_copy=props.use_copy
                )
                return True, f"Rebuilt {operator_type}"
        
        elif operator_type == "random_cables":
            wm = context.window_manager
            if hasattr(wm, 'random_cables_props'):
                props = wm.random_cables_props
                bpy.ops.mesh.random_cables(
                    seed=seed,
                    cable_type=props.cable_type,
                    count=props.count,
                    radius=props.radius,
                    slack=props.slack,
                    resolution=props.resolution,
                    length_min=props.length_min,
                    length_max=props.length_max
                )
                return True, f"Rebuilt {operator_type}"
        
        elif operator_type == "flanges":
            wm = context.window_manager
            if hasattr(wm, 'flanges_props'):
                props = wm.flanges_props
                bpy.ops.mesh.flanges(
                    seed=seed,
                    flange_size=props.flange_size,
                    flange_depth=props.flange_depth,
                    spacing=props.spacing,
                    probability=props.probability,
                    use_existing_curve=props.use_existing_curve
                )
                return True, f"Rebuilt {operator_type}"
        
        return False, f"Unknown operator type: {operator_type}"
