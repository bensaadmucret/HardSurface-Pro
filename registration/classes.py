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
Centralized class registration for the addon.
This module maintains a single list of all classes to register/unregister.
"""

import bpy

# Import all Blender registrable classes (Panels and Operators)
from ..ui.panels.main_panel import VIEW3D_PT_hardsurface_main
from ..ui.panels.panels_panel import VIEW3D_PT_hardsurface_panels
from ..ui.panels.extrude_panel import VIEW3D_PT_hardsurface_extrude
from ..ui.panels.scatter_panel import VIEW3D_PT_hardsurface_scatter
from ..ui.panels.tubes_panel import VIEW3D_PT_hardsurface_tubes
from ..ui.panels.presets_panel import VIEW3D_PT_hardsurface_presets
from ..ui.panels.utilities_panel import VIEW3D_PT_hardsurface_utilities
from ..ui.panels.loop_extrude_panel import VIEW3D_PT_hardsurface_loop_extrude
from ..ui.panels.screws_panel import VIEW3D_PT_hardsurface_screws
from ..ui.panels.axis_extrude_panel import VIEW3D_PT_hardsurface_axis_extrude
from ..ui.panels.cells_panel import VIEW3D_PT_hardsurface_cells
from ..ui.panels.cables_panel import VIEW3D_PT_hardsurface_cables
from ..ui.panels.flanges_panel import VIEW3D_PT_hardsurface_flanges
from ..operators.panels.op_random_panels import OBJECT_OT_random_panels
from ..operators.panels.op_panel_screws import OBJECT_OT_panel_screws
from ..operators.extrude.op_random_extrude import OBJECT_OT_random_extrude
from ..operators.extrude.op_random_loop_extrude import OBJECT_OT_random_loop_extrude
from ..operators.extrude.op_random_axis_extrude import OBJECT_OT_random_axis_extrude
from ..operators.scatter.op_random_scatter import OBJECT_OT_random_scatter
from ..operators.scatter.op_random_cells import OBJECT_OT_random_cells
from ..operators.tubes.op_random_tubes import OBJECT_OT_random_tubes
from ..operators.tubes.op_random_cables import OBJECT_OT_random_cables
from ..operators.tubes.op_flanges import OBJECT_OT_flanges
from ..operators.presets.op_save_preset import OBJECT_OT_save_preset
from ..operators.presets.op_load_preset import OBJECT_OT_load_preset
from ..operators.presets.op_delete_preset import OBJECT_OT_delete_preset
from ..operators.common.op_randomize_seed import OBJECT_OT_randomize_seed
from ..operators.common.op_reset_settings import OBJECT_OT_reset_settings
from ..operators.common.op_rebuild import OBJECT_OT_rebuild

# Define registration order (Panels and Operators only)
classes = [
    # Panels
    VIEW3D_PT_hardsurface_main,
    VIEW3D_PT_hardsurface_panels,
    VIEW3D_PT_hardsurface_extrude,
    VIEW3D_PT_hardsurface_scatter,
    VIEW3D_PT_hardsurface_tubes,
    VIEW3D_PT_hardsurface_loop_extrude,
    VIEW3D_PT_hardsurface_screws,
    VIEW3D_PT_hardsurface_axis_extrude,
    VIEW3D_PT_hardsurface_cells,
    VIEW3D_PT_hardsurface_cables,
    VIEW3D_PT_hardsurface_flanges,
    VIEW3D_PT_hardsurface_presets,
    VIEW3D_PT_hardsurface_utilities,
    # Operators
    OBJECT_OT_random_panels,
    OBJECT_OT_random_extrude,
    OBJECT_OT_random_scatter,
    OBJECT_OT_random_tubes,
    OBJECT_OT_random_loop_extrude,
    OBJECT_OT_random_axis_extrude,
    OBJECT_OT_panel_screws,
    OBJECT_OT_random_cells,
    OBJECT_OT_random_cables,
    OBJECT_OT_flanges,
    OBJECT_OT_save_preset,
    OBJECT_OT_load_preset,
    OBJECT_OT_delete_preset,
    OBJECT_OT_randomize_seed,
    OBJECT_OT_reset_settings,
    OBJECT_OT_rebuild,
]


def register():
    """Register all classes in the order they appear in the list."""
    for cls in classes:
        try:
            bpy.utils.register_class(cls)
        except ValueError:
            pass  # Already registered


def unregister():
    """Unregister all classes in reverse order."""
    for cls in reversed(classes):
        try:
            bpy.utils.unregister_class(cls)
        except RuntimeError:
            pass  # Not registered
