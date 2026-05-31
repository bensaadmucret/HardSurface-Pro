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
Enumerations for addon UI and operations.
Defines lists of options for various parameters.
"""


class Enums:
    """Enumerations for addon properties."""
    
    # Panel generation modes (for future use)
    PANEL_MODES = [
        ('INSET', 'Inset', 'Create inset panels'),
        ('EXTRUDE', 'Extrude', 'Create extruded panels'),
        ('BOTH', 'Both', 'Create both inset and extruded panels'),
    ]
    
    # Extrusion directions (for future use)
    EXTRUDE_DIRECTIONS = [
        ('NORMAL', 'Normal', 'Extrude along face normal'),
        ('CUSTOM', 'Custom', 'Extrude along custom vector'),
    ]
    
    # Scatter alignment modes (for future use)
    SCATTER_ALIGNMENTS = [
        ('NORMAL', 'Normal', 'Align to surface normal'),
        ('RANDOM', 'Random', 'Random rotation'),
        ('FIXED', 'Fixed', 'Fixed rotation'),
    ]
