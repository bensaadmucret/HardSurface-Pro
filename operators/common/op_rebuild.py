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
Rebuild operator.
Reapplies the last operation with stored parameters.
"""

import bpy
from bpy.types import Operator
from ...core.rebuild.rebuild_manager import RebuildManager
from ...utils.blender_utils import BlenderUtils


class OBJECT_OT_rebuild(Operator):
    """Rebuild the last operation"""
    bl_idname = "hardsurface.rebuild"
    bl_label = "Rebuild Last"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        """Execute the rebuild operation."""
        if not RebuildManager.can_rebuild(context):
            BlenderUtils.report_error(self, "No previous operation to rebuild")
            return {'CANCELLED'}
        
        success, message = RebuildManager.rebuild(context)
        
        if success:
            BlenderUtils.report_info(self, message)
            return {'FINISHED'}
        else:
            BlenderUtils.report_error(self, message)
            return {'CANCELLED'}
