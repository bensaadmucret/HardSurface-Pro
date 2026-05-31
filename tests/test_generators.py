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
from hardsurface_addon.core.generators.panels_generator import PanelsGenerator
from hardsurface_addon.core.generators.extrude_generator import ExtrudeGenerator

class TestPanelsGenerator(unittest.TestCase):
    """Test cases for PanelsGenerator."""
    
    def test_init_with_seed(self):
        """Test generator initializes with seed."""
        gen = PanelsGenerator(42)
        self.assertEqual(gen.seed, 42)
        self.assertIsNotNone(gen.rng)
    
    def test_get_config_dict(self):
        """Test config serialization."""
        gen = PanelsGenerator(123)
        config = gen.get_config_dict()
        self.assertEqual(config['seed'], 123)
        self.assertEqual(config['type'], 'random_panels')

class TestExtrudeGenerator(unittest.TestCase):
    """Test cases for ExtrudeGenerator."""
    
    def test_init_with_seed(self):
        """Test generator initializes with seed."""
        gen = ExtrudeGenerator(42)
        self.assertEqual(gen.seed, 42)

if __name__ == '__main__':
    unittest.main()
