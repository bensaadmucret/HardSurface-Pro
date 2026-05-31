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
Professional UI drawing utilities for HardSurface Pro.
Provides consistent styling matching professional addons like Random Slice.
"""

import bpy


class HardsurfaceUI:
    """Professional UI drawing helpers."""
    
    @staticmethod
    def draw_header(layout, title, icon='NONE'):
        """Draw a section header."""
        row = layout.row()
        row.label(text=title, icon=icon)
        row.scale_y = 1.2
    
    @staticmethod
    def draw_section(layout, title, icon='TRIA_DOWN'):
        """Draw a collapsible section box."""
        box = layout.box()
        row = box.row()
        row.label(text=title, icon=icon)
        return box
    
    @staticmethod
    def draw_label_value(layout, label, value_prop, icon='NONE'):
        """Draw a label with aligned value like Random Slice."""
        split = layout.split(factor=0.4)
        split.label(text=label)
        split.prop(value_prop, icon=icon, text="")
    
    @staticmethod
    def draw_min_max(layout, obj, min_prop, max_prop, label=""):
        """Draw Min/Max sliders side by side."""
        row = layout.row()
        if label:
            row.label(text=label)
            row = layout.row()
        
        split = row.split(factor=0.5)
        col = split.column()
        col.prop(obj, min_prop, text="Min")
        col = split.column()
        col.prop(obj, max_prop, text="Max")
    
    @staticmethod
    def draw_enum_buttons(layout, obj, prop_name, label=""):
        """Draw enum as horizontal buttons (radio style)."""
        if label:
            layout.label(text=label)
        row = layout.row(align=True)
        row.prop(obj, prop_name, expand=True)
    
    @staticmethod
    def draw_toggle_buttons(layout, obj, prop_name, label="", icons=None):
        """Draw boolean as On/Off buttons."""
        if label:
            layout.label(text=label)
        row = layout.row(align=True)
        row.prop(obj, prop_name, expand=True)
    
    @staticmethod
    def draw_seed_row(layout, obj, prop_name="seed"):
        """Draw seed with randomize button."""
        row = layout.row(align=True)
        row.prop(obj, prop_name, text="Seed")
        row.operator("hardsurface.randomize_seed", text="", icon='FILE_REFRESH')
    
    @staticmethod
    def draw_action_button(layout, operator_id, text, icon='PLAY'):
        """Draw a prominent action button."""
        row = layout.row()
        row.scale_y = 1.5
        row.operator(operator_id, text=text, icon=icon)
