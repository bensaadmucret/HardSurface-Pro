import sys
import os
from unittest.mock import MagicMock, patch

# Add parent directory to path for absolute imports
addon_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if addon_dir not in sys.path:
    sys.path.insert(0, addon_dir)

# Mock bpy so imports succeed outside Blender
sys.modules['bpy'] = MagicMock()
sys.modules['bmesh'] = MagicMock()
sys.modules['mathutils'] = MagicMock()

import unittest
from hardsurface_addon.services.seed_service import SeedService
from hardsurface_addon.services.selection_service import SelectionService

class TestSeedService(unittest.TestCase):
    """Test cases for SeedService."""
    
    def test_generate_returns_int(self):
        """Seed should always return an integer."""
        seed = SeedService.generate()
        self.assertIsInstance(seed, int)
        self.assertGreaterEqual(seed, 0)
    
    def test_generate_unique(self):
        """Generated seeds should be different."""
        seeds = {SeedService.generate() for _ in range(100)}
        self.assertGreater(len(seeds), 90, "Expected mostly unique seeds")

class TestSelectionService(unittest.TestCase):
    """Test cases for SelectionService."""
    
    def test_validate_face_selection_no_object(self):
        """No object should return invalid."""
        is_valid, error = SelectionService.validate_face_selection(None)
        self.assertFalse(is_valid)
        self.assertIn("No active object", error)

if __name__ == '__main__':
    unittest.main()
