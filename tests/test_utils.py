import sys
import os
from unittest.mock import MagicMock, PropertyMock

# Add parent directory to path for absolute imports
addon_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if addon_dir not in sys.path:
    sys.path.insert(0, addon_dir)

# Mock bpy and bmesh so imports succeed outside Blender
sys.modules['bpy'] = MagicMock()
sys.modules['bmesh'] = MagicMock()
sys.modules['mathutils'] = MagicMock()

import unittest
from hardsurface_addon.utils.math_utils import MathUtils
from hardsurface_addon.utils.naming import NamingUtils

class TestMathUtils(unittest.TestCase):
    """Test cases for MathUtils class."""
    
    def test_lerp(self):
        """Test linear interpolation."""
        self.assertEqual(MathUtils.lerp(0.0, 10.0, 0.5), 5.0)
        self.assertEqual(MathUtils.lerp(0.0, 10.0, 0.0), 0.0)
        self.assertEqual(MathUtils.lerp(0.0, 10.0, 1.0), 10.0)
        
    def test_clamp(self):
        """Test value clamping."""
        self.assertEqual(MathUtils.clamp(5.0, 0.0, 10.0), 5.0)
        self.assertEqual(MathUtils.clamp(-5.0, 0.0, 10.0), 0.0)
        self.assertEqual(MathUtils.clamp(15.0, 0.0, 10.0), 10.0)
    
    def test_map_range(self):
        """Test range mapping."""
        self.assertEqual(MathUtils.map_range(5.0, 0.0, 10.0, 0.0, 100.0), 50.0)
        self.assertEqual(MathUtils.map_range(0.0, 0.0, 10.0, 0.0, 100.0), 0.0)
        self.assertEqual(MathUtils.map_range(10.0, 0.0, 10.0, 0.0, 100.0), 100.0)

class TestNamingUtils(unittest.TestCase):
    """Test cases for NamingUtils utility."""
    
    def test_generate_name(self):
        """Test name generation with prefix."""
        name = NamingUtils.generate_name("HS_Panels", "Test")
        self.assertEqual(name, "HS_Panels_Test")
    
    def test_generate_name_without_base(self):
        """Test name generation without base name."""
        name = NamingUtils.generate_name("HS_Panels")
        self.assertEqual(name, "HS_Panels")
    
    def test_prefixes(self):
        """Test that prefixes are defined."""
        self.assertEqual(NamingUtils.PREFIX_PANELS, "HS_Panels")
        self.assertEqual(NamingUtils.PREFIX_EXTRUDE, "HS_Extrude")

if __name__ == '__main__':
    unittest.main()
