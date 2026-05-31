# HardSurface Pro

Procedural hard-surface generation addon for Blender.

## Features

- **Random Panels**: Generate random inset panels on selected faces with configurable probability, inset depth, and extrusion depth.
- **Random Extrude**: Create random extrusions with height variation, taper effects, and face count limiting.
- **Random Scatter**: Distribute objects from a collection on a target surface with density, rotation, and scale controls.
- **Random Tubes**: Generate tubes from selected edges with radius variation and segment control.
- **Seed System**: Reproducible results with seed-based randomization.
- **Rebuild**: Reapply the last operation with stored parameters.
- **Presets**: Save, load, and delete parameter presets for quick workflow.
- **Utilities**: Randomize seed, reset settings to defaults.

## Installation

1. Download `hardsurface_addon_v1.0.0.zip` or the `hardsurface_addon` folder.
2. In Blender, go to `Edit > Preferences > Add-ons > Install...`
3. Navigate to and select the zip file or folder.
4. Enable the addon by checking the box next to "HardSurface Pro".

## Requirements

- Blender 3.6 or higher

## Usage

### Random Panels

1. Select a mesh object and enter Edit Mode.
2. Select the faces you want to apply panels to.
3. In the N-Panel (View 3D > Sidebar), find the "HardSurface" tab.
4. Expand "Random Panels".
5. Adjust parameters (seed, probability, inset min/max, depth min/max).
6. Click "Random Panels" to generate.

### Random Extrude

1. Select a mesh object and enter Edit Mode.
2. Select the faces you want to extrude.
3. In the N-Panel, expand "Random Extrude".
4. Adjust parameters (seed, extrude rate, height min/max, taper min/max).
5. Click "Random Extrude" to generate.

### Random Scatter

1. Create a collection with mesh objects you want to scatter.
2. Select a target mesh object (Object Mode).
3. In the N-Panel, expand "Random Scatter".
4. Select the source collection.
5. Adjust parameters (density, rotation, scale, alignment).
6. Click "Random Scatter" to distribute objects.

### Random Tubes

1. Select a mesh object and enter Edit Mode.
2. Select the edges you want to convert to tubes.
3. In the N-Panel, expand "Random Tubes".
4. Adjust parameters (radius, radius variation, segments).
5. Click "Random Tubes" to generate.

### Seed System

- Each operation uses a seed for reproducible results.
- Click the refresh icon next to the seed to generate a new random seed.
- The last operation's seed is stored for rebuild functionality.

### Rebuild

- Use the "Rebuild Last" button in the Utilities panel to reapply the last operation with the same parameters.
- This allows you to regenerate results without changing settings.

### Presets

- **Save Preset**: After configuring parameters, click "Save Preset" to store them with a custom name.
- **Load Preset**: Click "Load Preset" to apply a saved preset to the current operator.
- **Delete Preset**: Remove unwanted presets from the preset library.
- Presets are stored in Blender's scripts directory under `presets/hardsurface/`.

## Architecture

The addon follows a modular architecture:

```
hardsurface_addon/
├── registration/      # Class registration system
├── preferences/       # Addon preferences
├── properties/        # PropertyGroups for parameters
├── ui/               # N-Panel UI
├── operators/        # Blender operators
├── core/             # Business logic
│   ├── generators/   # Generation orchestration
│   ├── algorithms/   # Low-level algorithms
│   ├── rebuild/      # Rebuild system
│   └── validation/   # Context validation
├── services/         # Transverse services
├── utils/            # Technical utilities
└── data/             # Constants and defaults
```

## License

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

See the [LICENSE](LICENSE) file for details.

## Version

Current version: 1.0.0
