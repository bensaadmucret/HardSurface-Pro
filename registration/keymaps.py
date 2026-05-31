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
Keymap registration for the addon.
Optional keyboard shortcuts for quick access to main operators.
"""

import bpy


# Store keymaps for unregistration
_keymaps = []


def register():
    """Register addon keymaps."""
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    
    if kc:
        # Random Panels: Ctrl+Shift+P
        km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new('mesh.random_panels', 'P', 'PRESS', ctrl=True, shift=True)
        _keymaps.append((km, kmi))
        
        # Random Extrude: Ctrl+Shift+E
        km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new('mesh.random_extrude', 'E', 'PRESS', ctrl=True, shift=True)
        _keymaps.append((km, kmi))
        
        # Random Scatter: Ctrl+Shift+S
        km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new('mesh.random_scatter', 'S', 'PRESS', ctrl=True, shift=True)
        _keymaps.append((km, kmi))
        
        # Random Tubes: Ctrl+Shift+T
        km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new('mesh.random_tubes', 'T', 'PRESS', ctrl=True, shift=True)
        _keymaps.append((km, kmi))
        
        # Rebuild Last: Ctrl+Shift+R
        km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new('hardsurface.rebuild', 'R', 'PRESS', ctrl=True, shift=True)
        _keymaps.append((km, kmi))
        
        # Randomize Seed: Ctrl+Shift+Z
        km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new('hardsurface.randomize_seed', 'Z', 'PRESS', ctrl=True, shift=True)
        _keymaps.append((km, kmi))


def unregister():
    """Unregister addon keymaps."""
    for km, kmi in _keymaps:
        km.keymap_items.remove(kmi)
    _keymaps.clear()
