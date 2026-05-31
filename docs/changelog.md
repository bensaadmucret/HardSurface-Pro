# Changelog

All notable changes to HardSurface Pro will be documented in this file.

## [1.0.0] - 2026-05-30

### Added
- **Random Panels**: Generate random inset panels on selected faces with configurable probability, inset depth, and extrusion depth
- **Random Extrude**: Create random extrusions with height variation, taper effects, and face count limiting
- **Random Scatter**: Distribute objects from a collection on a target surface with density, rotation, and scale controls
- **Random Tubes**: Generate tubes from selected edges with radius variation and segment control
- **Seed System**: Reproducible results with seed-based randomization
- **Rebuild**: Reapply the last operation with stored parameters
- **Presets**: Save, load, and delete parameter presets for quick workflow
- **Utilities**: Randomize seed, reset settings to defaults
- **N-Panel UI**: Complete interface in Blender's sidebar with all operators
- **Modular Architecture**: Clean separation of UI, operators, core logic, services, and utilities

### Features
- Barycentric coordinate sampling for uniform point distribution on faces
- PropertyGroups for parameter persistence
- Centralized class registration system
- Preset storage in Blender's scripts directory
- Comprehensive validation for mesh objects and selections
- Logging system for debugging

### Technical
- Compatible with Blender 3.6+
- Python-based addon using bpy, bmesh, and mathutils
- No external dependencies required
- JSON-based preset system with versioning
