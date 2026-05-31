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
Operator properties for Random Panels, Random Extrude, Random Scatter, and Random Tubes.
These properties are used by the operators and can be serialized for presets.
"""

import bpy
from bpy.props import (
    IntProperty,
    FloatProperty,
    BoolProperty,
    FloatVectorProperty,
    StringProperty,
    CollectionProperty,
    EnumProperty
)


class RandomPanelsProps(bpy.types.PropertyGroup):
    """Properties for Random Panels operator."""
    
    seed: IntProperty(
        name="Seed",
        description="Random seed for reproducible results",
        default=0,
        min=0
    )
    
    probability: FloatProperty(
        name="Probability",
        description="Probability of applying panel to each face",
        default=0.5,
        min=0.0,
        max=1.0
    )
    
    inset_min: FloatProperty(
        name="Inset Min",
        description="Minimum inset amount",
        default=0.02,
        min=0.0,
        max=1.0
    )
    
    inset_max: FloatProperty(
        name="Inset Max",
        description="Maximum inset amount",
        default=0.1,
        min=0.0,
        max=1.0
    )
    
    depth_min: FloatProperty(
        name="Depth Min",
        description="Minimum extrusion depth",
        default=-0.05,
        min=-1.0,
        max=1.0
    )
    
    depth_max: FloatProperty(
        name="Depth Max",
        description="Maximum extrusion depth",
        default=0.05,
        min=-1.0,
        max=1.0
    )
    
    safety_margin: FloatProperty(
        name="Safety Margin",
        description="Margin to avoid visual collisions",
        default=0.01,
        min=0.0,
        max=0.5
    )
    
    use_copy: BoolProperty(
        name="Use Copy",
        description="Apply on a copy of the object",
        default=False
    )
    
    use_materials: BoolProperty(
        name="Valley Materials",
        description="Assign second material slot to panel valleys",
        default=True
    )
    
    bevel_amount: FloatProperty(
        name="Bevel Amount",
        description="Bevel width for panel cap edges",
        default=0.0,
        min=0.0,
        max=0.1
    )
    
    solver_mode: EnumProperty(
        name="Solver",
        description="Face selection solver mode",
        items=[
            ('RANDOM', "Random", "Random face selection"),
            ('SHORTEST', "Shortest", "Prioritize shortest edges"),
        ],
        default='RANDOM'
    )
    
    direction_mode: EnumProperty(
        name="Direction",
        description="Inset direction mode",
        items=[
            ('TANGENT', "Tangent", "Follow face tangent"),
            ('PER_FACE', "Per Face", "Individual face direction"),
        ],
        default='TANGENT'
    )
    
    axis_mode: EnumProperty(
        name="Axis",
        description="Primary axis for panel generation",
        items=[
            ('XYZ', "XYZ", "All axes"),
            ('X', "X", "X axis only"),
            ('Y', "Y", "Y axis only"),
            ('Z', "Z", "Z axis only"),
        ],
        default='XYZ'
    )
    
    view_mode: EnumProperty(
        name="View",
        description="View-based or global generation",
        items=[
            ('VIEW', "View", "From current view"),
            ('GLOBAL', "Global", "Global coordinates"),
        ],
        default='GLOBAL'
    )


class RandomExtrudeProps(bpy.types.PropertyGroup):
    """Properties for Random Extrude operator."""
    
    seed: IntProperty(
        name="Seed",
        description="Random seed for reproducible results",
        default=0,
        min=0
    )
    
    extrude_rate: FloatProperty(
        name="Extrude Rate",
        description="Rate of face extrusion",
        default=0.5,
        min=0.0,
        max=1.0
    )
    
    height_min: FloatProperty(
        name="Height Min",
        description="Minimum extrusion height",
        default=0.2,
        min=0.0,
        max=10.0
    )
    
    height_max: FloatProperty(
        name="Height Max",
        description="Maximum extrusion height",
        default=1.0,
        min=0.0,
        max=10.0
    )
    
    taper_min: FloatProperty(
        name="Taper Min",
        description="Minimum taper amount (0 = no taper)",
        default=0.0,
        min=0.0,
        max=1.0
    )
    
    taper_max: FloatProperty(
        name="Taper Max",
        description="Maximum taper amount (1 = point, 0 = no taper)",
        default=0.2,
        min=0.0,
        max=1.0
    )
    
    max_faces: IntProperty(
        name="Max Faces",
        description="Maximum number of faces to affect",
        default=100,
        min=1,
        max=10000
    )
    
    group_islands: BoolProperty(
        name="Group Islands",
        description="Group affected faces by islands",
        default=False
    )


class RandomScatterProps(bpy.types.PropertyGroup):
    """Properties for Random Scatter operator."""
    
    seed: IntProperty(
        name="Seed",
        description="Random seed for reproducible results",
        default=0,
        min=0
    )
    
    collection_name: StringProperty(
        name="Collection",
        description="Source collection of objects to scatter",
        default=""
    )
    
    density: FloatProperty(
        name="Density",
        description="Number of objects per unit area",
        default=1.0,
        min=0.1,
        max=100.0
    )
    
    rotation_min: FloatProperty(
        name="Rotation Min",
        description="Minimum random rotation (degrees)",
        default=0.0,
        min=0.0,
        max=360.0
    )
    
    rotation_max: FloatProperty(
        name="Rotation Max",
        description="Maximum random rotation (degrees)",
        default=360.0,
        min=0.0,
        max=360.0
    )
    
    scale_min: FloatProperty(
        name="Scale Min",
        description="Minimum random scale",
        default=0.5,
        min=0.1,
        max=10.0
    )
    
    scale_max: FloatProperty(
        name="Scale Max",
        description="Maximum random scale",
        default=1.5,
        min=0.1,
        max=10.0
    )
    
    align_to_normal: BoolProperty(
        name="Align to Normal",
        description="Align objects to surface normal",
        default=True
    )
    
    surface_offset: FloatProperty(
        name="Surface Offset",
        description="Offset from surface",
        default=0.0,
        min=-10.0,
        max=10.0
    )


class RandomTubesProps(bpy.types.PropertyGroup):
    """Properties for Random Tubes operator."""
    
    seed: IntProperty(
        name="Seed",
        description="Random seed for reproducible results",
        default=0,
        min=0
    )
    
    radius: FloatProperty(
        name="Radius",
        description="Base radius of tubes",
        default=0.1,
        min=0.01,
        max=10.0
    )
    
    radius_variation: FloatProperty(
        name="Radius Variation",
        description="Amount of radius variation",
        default=0.5,
        min=0.0,
        max=1.0
    )
    
    segments: IntProperty(
        name="Segments",
        description="Number of segments per tube",
        default=16,
        min=3,
        max=64
    )
    
    smooth: BoolProperty(
        name="Smooth",
        description="Apply smooth shading to tubes",
        default=True
    )


class RandomLoopExtrudeProps(bpy.types.PropertyGroup):
    """Properties for Random Loop Extrude (Greeble Stacks) operator."""
    
    seed: IntProperty(
        name="Seed",
        description="Random seed for reproducible results",
        default=0,
        min=0
    )
    
    iterations: IntProperty(
        name="Iterations",
        description="Number of recursive inset/extrude iterations",
        default=2,
        min=1,
        max=6
    )
    
    probability: FloatProperty(
        name="Probability",
        description="Probability of applying to each face per iteration",
        default=0.7,
        min=0.0,
        max=1.0
    )
    
    height_min: FloatProperty(
        name="Height Min",
        description="Minimum extrusion height",
        default=0.05,
        min=0.0,
        max=1.0
    )
    
    height_max: FloatProperty(
        name="Height Max",
        description="Maximum extrusion height",
        default=0.3,
        min=0.0,
        max=1.0
    )
    
    height_decay: FloatProperty(
        name="Height Decay",
        description="Factor to reduce height each iteration",
        default=0.7,
        min=0.1,
        max=1.0
    )
    
    inset_min: FloatProperty(
        name="Inset Min",
        description="Minimum inset amount",
        default=0.02,
        min=0.0,
        max=1.0
    )
    
    inset_max: FloatProperty(
        name="Inset Max",
        description="Maximum inset amount",
        default=0.1,
        min=0.0,
        max=1.0
    )
    
    taper: FloatProperty(
        name="Taper",
        description="Taper factor for each iteration",
        default=0.0,
        min=0.0,
        max=1.0
    )
    
    use_copy: BoolProperty(
        name="Use Copy",
        description="Apply on a copy of the object",
        default=False
    )


class PanelScrewsProps(bpy.types.PropertyGroup):
    """Properties for Panel Screws operator."""
    
    seed: IntProperty(
        name="Seed",
        description="Random seed for reproducible results",
        default=0,
        min=0
    )
    
    screw_size: FloatProperty(
        name="Screw Size",
        description="Size of the screw head",
        default=0.02,
        min=0.001,
        max=0.5
    )
    
    screw_depth: FloatProperty(
        name="Screw Depth",
        description="Depth the screw is embedded",
        default=0.005,
        min=0.0,
        max=0.1
    )
    
    probability: FloatProperty(
        name="Probability",
        description="Probability of placing a screw at each corner",
        default=0.8,
        min=0.0,
        max=1.0
    )
    
    screw_type: IntProperty(
        name="Screw Type",
        description="Type of screw head (0=Cylinder, 1=Hex, 2=Cone)",
        default=0,
        min=0,
        max=2
    )


class RandomAxisExtrudeProps(bpy.types.PropertyGroup):
    """Properties for Random Axis Extrude operator."""
    
    seed: IntProperty(
        name="Seed",
        description="Random seed for reproducible results",
        default=0,
        min=0
    )
    
    iterations: IntProperty(
        name="Iterations",
        description="Number of recursive branching iterations",
        default=2,
        min=1,
        max=5
    )
    
    probability_x: FloatProperty(
        name="X Probability",
        description="Probability of extruding in X axis",
        default=0.5,
        min=0.0,
        max=1.0
    )
    
    probability_y: FloatProperty(
        name="Y Probability",
        description="Probability of extruding in Y axis",
        default=0.5,
        min=0.0,
        max=1.0
    )
    
    probability_z: FloatProperty(
        name="Z Probability",
        description="Probability of extruding in Z axis",
        default=0.5,
        min=0.0,
        max=1.0
    )
    
    length_min: FloatProperty(
        name="Length Min",
        description="Minimum extrusion length",
        default=0.1,
        min=0.01,
        max=5.0
    )
    
    length_max: FloatProperty(
        name="Length Max",
        description="Maximum extrusion length",
        default=0.5,
        min=0.01,
        max=5.0
    )
    
    scale_decay: FloatProperty(
        name="Scale Decay",
        description="Scale reduction each iteration",
        default=0.7,
        min=0.1,
        max=1.0
    )
    
    use_copy: BoolProperty(
        name="Use Copy",
        description="Apply on a copy of the object",
        default=False
    )


class RandomCellsProps(bpy.types.PropertyGroup):
    """Properties for Random Cells operator (emission planes / antennae)."""
    
    seed: IntProperty(
        name="Seed",
        description="Random seed for reproducible results",
        default=0,
        min=0
    )
    
    cell_type: EnumProperty(
        name="Cell Type",
        description="Type of cell to generate",
        items=[
            ('PLANE', "Plane", "Flat emission plane"),
            ('ANTENNA', "Antenna", "Thin extruded antenna"),
            ('BOX', "Box", "Small box protrusion"),
        ],
        default='PLANE'
    )
    
    density: FloatProperty(
        name="Density",
        description="Number of cells per unit area",
        default=0.3,
        min=0.0,
        max=1.0
    )
    
    size_min: FloatProperty(
        name="Size Min",
        description="Minimum cell size",
        default=0.05,
        min=0.01,
        max=1.0
    )
    
    size_max: FloatProperty(
        name="Size Max",
        description="Maximum cell size",
        default=0.2,
        min=0.01,
        max=1.0
    )
    
    height_min: FloatProperty(
        name="Height Min",
        description="Minimum extrusion height (for antennae/boxes)",
        default=0.1,
        min=0.0,
        max=2.0
    )
    
    height_max: FloatProperty(
        name="Height Max",
        description="Maximum extrusion height",
        default=0.5,
        min=0.0,
        max=2.0
    )
    
    align_to_normal: BoolProperty(
        name="Align to Normal",
        description="Align cells to face normal",
        default=True
    )
    
    use_copy: BoolProperty(
        name="Use Copy",
        description="Apply on a copy of the object",
        default=False
    )


class RandomCablesProps(bpy.types.PropertyGroup):
    """Properties for Random Cables operator."""
    
    seed: IntProperty(
        name="Seed",
        description="Random seed for reproducible results",
        default=0,
        min=0
    )
    
    cable_type: EnumProperty(
        name="Cable Type",
        description="Type of cable curve",
        items=[
            ('CATENARY', "Catenary", "Hanging cable curve"),
            ('BEZIER', "Bezier", "Manual bezier curve"),
            ('STRAIGHT', "Straight", "Straight line cable"),
        ],
        default='CATENARY'
    )
    
    count: IntProperty(
        name="Count",
        description="Number of cables to create",
        default=3,
        min=1,
        max=50
    )
    
    radius: FloatProperty(
        name="Radius",
        description="Cable thickness radius",
        default=0.02,
        min=0.001,
        max=0.5
    )
    
    slack: FloatProperty(
        name="Slack",
        description="Amount of cable slack (catenary depth)",
        default=0.3,
        min=0.0,
        max=2.0
    )
    
    resolution: IntProperty(
        name="Resolution",
        description="Points per cable",
        default=12,
        min=3,
        max=64
    )
    
    length_min: FloatProperty(
        name="Length Min",
        description="Minimum cable length",
        default=1.0,
        min=0.1,
        max=10.0
    )
    
    length_max: FloatProperty(
        name="Length Max",
        description="Maximum cable length",
        default=3.0,
        min=0.1,
        max=10.0
    )


class FlangesProps(bpy.types.PropertyGroup):
    """Properties for Flanges/Couplings operator."""
    
    seed: IntProperty(
        name="Seed",
        description="Random seed for reproducible results",
        default=0,
        min=0
    )
    
    flange_size: FloatProperty(
        name="Flange Size",
        description="Radius of the flange coupling",
        default=0.05,
        min=0.01,
        max=0.5
    )
    
    flange_depth: FloatProperty(
        name="Flange Depth",
        description="Thickness of the flange",
        default=0.02,
        min=0.005,
        max=0.2
    )
    
    spacing: FloatProperty(
        name="Spacing",
        description="Distance between flanges along curve",
        default=0.5,
        min=0.1,
        max=5.0
    )
    
    probability: FloatProperty(
        name="Probability",
        description="Chance of placing a flange at each point",
        default=0.8,
        min=0.0,
        max=1.0
    )
    
    use_existing_curve: BoolProperty(
        name="Use Existing Curve",
        description="Use selected curve object instead of creating new",
        default=False
    )


class NoiseDisplaceProps(bpy.types.PropertyGroup):
    """Properties for Noise Displace operator."""

    seed: IntProperty(
        name="Seed",
        description="Noise seed",
        default=0,
        min=0,
        max=2147483647
    )

    scale: FloatProperty(
        name="Scale",
        description="Scale of the noise",
        default=2.0,
        min=0.001,
        max=100.0
    )

    strength: FloatProperty(
        name="Strength",
        description="Displacement strength",
        default=0.5,
        min=0.0,
        max=10.0
    )

    detail: FloatProperty(
        name="Detail",
        description="Noise detail / octaves",
        default=2.0,
        min=0.0,
        max=16.0
    )

    noise_type: EnumProperty(
        name="Noise Type",
        items=[
            ('PERLIN', "Perlin", "Classic Perlin noise"),
            ('VORONOI_F1', "Voronoi F1", "Voronoi distance to nearest cell center"),
            ('VORONOI_F2', "Voronoi F2", "Voronoi distance to 2nd nearest cell center"),
            ('VORONOI_F2F1', "Voronoi F2-F1", "Difference between F2 and F1"),
            ('CELLNOISE', "Cell Noise", "Cell-based noise"),
            ('SIMPLEX', "Simplex", "Simplex noise"),
        ],
        default='PERLIN'
    )

    use_normal: BoolProperty(
        name="Along Normal",
        description="Displace along vertex normals",
        default=True
    )

    axis: EnumProperty(
        name="Axis",
        items=[
            ('X', "X", "Local X axis"),
            ('Y', "Y", "Local Y axis"),
            ('Z', "Z", "Local Z axis"),
        ],
        default='Z'
    )

    smooth: BoolProperty(
        name="Smooth",
        description="Use smooth interpolation",
        default=True
    )


class ImageDisplaceProps(bpy.types.PropertyGroup):
    """Properties for Image Displace operator."""

    image_path: StringProperty(
        name="Image",
        description="Path to the image texture",
        default="",
        subtype='FILE_PATH'
    )

    strength: FloatProperty(
        name="Strength",
        description="Displacement strength",
        default=1.0,
        min=-10.0,
        max=10.0
    )

    use_normal: BoolProperty(
        name="Along Normal",
        description="Displace along vertex normals",
        default=True
    )

    axis: EnumProperty(
        name="Axis",
        items=[
            ('X', "X", "Local X axis"),
            ('Y', "Y", "Local Y axis"),
            ('Z', "Z", "Local Z axis"),
        ],
        default='Z'
    )

    channel: EnumProperty(
        name="Channel",
        items=[
            ('LUMINANCE', "Luminance", "Grayscale luminance"),
            ('RED', "Red", "Red channel"),
            ('GREEN', "Green", "Green channel"),
            ('BLUE', "Blue", "Blue channel"),
            ('ALPHA', "Alpha", "Alpha channel"),
        ],
        default='LUMINANCE'
    )

    use_uv: BoolProperty(
        name="Use UV",
        description="Map image using active UV map instead of planar projection",
        default=True
    )


def register():
    # Register the PropertyGroup classes first
    for cls in [RandomPanelsProps, RandomExtrudeProps, RandomScatterProps, RandomTubesProps,
                RandomLoopExtrudeProps, PanelScrewsProps, RandomAxisExtrudeProps, RandomCellsProps,
                RandomCablesProps, FlangesProps, NoiseDisplaceProps, ImageDisplaceProps]:
        try:
            bpy.utils.register_class(cls)
        except ValueError:
            pass
            
    if not hasattr(bpy.types.WindowManager, 'random_panels_props'):
        bpy.types.WindowManager.random_panels_props = bpy.props.PointerProperty(
            type=RandomPanelsProps
        )
    if not hasattr(bpy.types.WindowManager, 'random_extrude_props'):
        bpy.types.WindowManager.random_extrude_props = bpy.props.PointerProperty(
            type=RandomExtrudeProps
        )
    if not hasattr(bpy.types.WindowManager, 'random_scatter_props'):
        bpy.types.WindowManager.random_scatter_props = bpy.props.PointerProperty(
            type=RandomScatterProps
        )
    if not hasattr(bpy.types.WindowManager, 'random_tubes_props'):
        bpy.types.WindowManager.random_tubes_props = bpy.props.PointerProperty(
            type=RandomTubesProps
        )
    if not hasattr(bpy.types.WindowManager, 'random_loop_extrude_props'):
        bpy.types.WindowManager.random_loop_extrude_props = bpy.props.PointerProperty(
            type=RandomLoopExtrudeProps
        )
    if not hasattr(bpy.types.WindowManager, 'panel_screws_props'):
        bpy.types.WindowManager.panel_screws_props = bpy.props.PointerProperty(
            type=PanelScrewsProps
        )
    if not hasattr(bpy.types.WindowManager, 'random_axis_extrude_props'):
        bpy.types.WindowManager.random_axis_extrude_props = bpy.props.PointerProperty(
            type=RandomAxisExtrudeProps
        )
    if not hasattr(bpy.types.WindowManager, 'random_cells_props'):
        bpy.types.WindowManager.random_cells_props = bpy.props.PointerProperty(
            type=RandomCellsProps
        )
    if not hasattr(bpy.types.WindowManager, 'random_cables_props'):
        bpy.types.WindowManager.random_cables_props = bpy.props.PointerProperty(
            type=RandomCablesProps
        )
    if not hasattr(bpy.types.WindowManager, 'flanges_props'):
        bpy.types.WindowManager.flanges_props = bpy.props.PointerProperty(
            type=FlangesProps
        )
    if not hasattr(bpy.types.WindowManager, 'noise_displace_props'):
        bpy.types.WindowManager.noise_displace_props = bpy.props.PointerProperty(
            type=NoiseDisplaceProps
        )
    if not hasattr(bpy.types.WindowManager, 'image_displace_props'):
        bpy.types.WindowManager.image_displace_props = bpy.props.PointerProperty(
            type=ImageDisplaceProps
        )


def unregister():
    if hasattr(bpy.types.WindowManager, 'random_panels_props'):
        del bpy.types.WindowManager.random_panels_props
    if hasattr(bpy.types.WindowManager, 'random_extrude_props'):
        del bpy.types.WindowManager.random_extrude_props
    if hasattr(bpy.types.WindowManager, 'random_scatter_props'):
        del bpy.types.WindowManager.random_scatter_props
    if hasattr(bpy.types.WindowManager, 'random_tubes_props'):
        del bpy.types.WindowManager.random_tubes_props
    if hasattr(bpy.types.WindowManager, 'random_loop_extrude_props'):
        del bpy.types.WindowManager.random_loop_extrude_props
    if hasattr(bpy.types.WindowManager, 'panel_screws_props'):
        del bpy.types.WindowManager.panel_screws_props
    if hasattr(bpy.types.WindowManager, 'random_axis_extrude_props'):
        del bpy.types.WindowManager.random_axis_extrude_props
    if hasattr(bpy.types.WindowManager, 'random_cells_props'):
        del bpy.types.WindowManager.random_cells_props
    if hasattr(bpy.types.WindowManager, 'random_cables_props'):
        del bpy.types.WindowManager.random_cables_props
    if hasattr(bpy.types.WindowManager, 'flanges_props'):
        del bpy.types.WindowManager.flanges_props
    if hasattr(bpy.types.WindowManager, 'noise_displace_props'):
        del bpy.types.WindowManager.noise_displace_props
    if hasattr(bpy.types.WindowManager, 'image_displace_props'):
        del bpy.types.WindowManager.image_displace_props

    # Unregister PropertyGroup classes last
    for cls in reversed([RandomPanelsProps, RandomExtrudeProps, RandomScatterProps, RandomTubesProps,
                         RandomLoopExtrudeProps, PanelScrewsProps, RandomAxisExtrudeProps, RandomCellsProps,
                         RandomCablesProps, FlangesProps, NoiseDisplaceProps, ImageDisplaceProps]):
        try:
            bpy.utils.unregister_class(cls)
        except RuntimeError:
            pass
