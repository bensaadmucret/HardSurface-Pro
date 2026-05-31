import sys
import os
from unittest.mock import MagicMock, patch

# Add parent directory to path for absolute imports
addon_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if addon_dir not in sys.path:
    sys.path.insert(0, addon_dir)

# Mock all Blender modules
sys.modules['bpy'] = MagicMock()
sys.modules['bmesh'] = MagicMock()
sys.modules['mathutils'] = MagicMock()
sys.modules['bpy.types'] = MagicMock()
sys.modules['bpy.props'] = MagicMock()

import unittest

class TestPropertyGroups(unittest.TestCase):
    """Test cases for PropertyGroup definitions."""
    
    def test_random_panels_props_class_exists(self):
        """Test RandomPanelsProps class exists."""
        from hardsurface_addon.properties.operator_props import RandomPanelsProps
        self.assertIsNotNone(RandomPanelsProps)
    
    def test_random_extrude_props_class_exists(self):
        """Test RandomExtrudeProps class exists."""
        from hardsurface_addon.properties.operator_props import RandomExtrudeProps
        self.assertIsNotNone(RandomExtrudeProps)

class TestSceneProps(unittest.TestCase):
    """Test cases for Scene-level properties."""
    
    def test_scene_props_class_exists(self):
        """Test HardSurfaceSceneProps class exists."""
        from hardsurface_addon.properties.scene_props import HardSurfaceSceneProps
        self.assertIsNotNone(HardSurfaceSceneProps)

if __name__ == '__main__':
    unittest.main()
