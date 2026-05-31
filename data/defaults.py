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
Default values for addon properties.
Centralized location for default parameter values.
"""


class Defaults:
    """Default values for addon properties."""
    
    # Random Panels defaults
    PANELS_SEED = 0
    PANELS_PROBABILITY = 0.5
    PANELS_INSET_MIN = 0.02
    PANELS_INSET_MAX = 0.1
    PANELS_DEPTH_MIN = -0.05
    PANELS_DEPTH_MAX = 0.05
    PANELS_SAFETY_MARGIN = 0.01
    PANELS_USE_COPY = False
    
    # Random Extrude defaults
    EXTRUDE_SEED = 0
    EXTRUDE_RATE = 0.5
    EXTRUDE_HEIGHT_MIN = 0.1
    EXTRUDE_HEIGHT_MAX = 0.5
    EXTRUDE_TAPER_MIN = 0.0
    EXTRUDE_TAPER_MAX = 0.5
    EXTRUDE_MAX_FACES = 100
    EXTRUDE_GROUP_ISLANDS = False
