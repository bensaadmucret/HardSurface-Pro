import sys
import os
from unittest.mock import MagicMock

# Add parent directory to path for absolute imports
addon_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if addon_dir not in sys.path:
    sys.path.insert(0, addon_dir)

# Mock bpy and bmesh so imports succeed outside Blender
sys.modules['bpy'] = MagicMock()
sys.modules['bmesh'] = MagicMock()

import unittest
from hardsurface_addon.utils.math_utils import MathUtils
from hardsurface_addon.core.algorithms.randomization import Randomization

class TestMathUtils(unittest.TestCase):
    """Test cases for MathUtils class."""
    
    def test_lerp(self):
        self.assertEqual(MathUtils.lerp(0.0, 10.0, 0.5), 5.0)
        self.assertEqual(MathUtils.lerp(0.0, 10.0, 0.0), 0.0)
        self.assertEqual(MathUtils.lerp(0.0, 10.0, 1.0), 10.0)
        
    def test_clamp(self):
        self.assertEqual(MathUtils.clamp(5.0, 0.0, 10.0), 5.0)
        self.assertEqual(MathUtils.clamp(-5.0, 0.0, 10.0), 0.0)
        self.assertEqual(MathUtils.clamp(15.0, 0.0, 10.0), 10.0)

class TestRandomization(unittest.TestCase):
    """Test cases for Randomization class."""
    
    def test_reproducibility(self):
        # Two randomizations with the same seed should yield same sequences
        rng1 = Randomization(42)
        rng2 = Randomization(42)
        
        self.assertEqual(rng1.random_float(0.0, 1.0), rng2.random_float(0.0, 1.0))
        self.assertEqual(rng1.random_int(1, 100), rng2.random_int(1, 100))
        self.assertEqual(rng1.random_bool(0.5), rng2.random_bool(0.5))
        
        items = ["a", "b", "c", "d", "e"]
        self.assertEqual(rng1.shuffle(items), rng2.shuffle(items))
        self.assertEqual(rng1.random_subset(items, 3), rng2.random_subset(items, 3))

if __name__ == '__main__':
    unittest.main()
