import sys
import os
from unittest.mock import MagicMock

# Add parent directory to path for absolute imports
addon_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if addon_dir not in sys.path:
    sys.path.insert(0, addon_dir)

import unittest
from hardsurface_addon.core.algorithms.randomization import Randomization
from hardsurface_addon.core.algorithms.extrude_ops import ExtrusionOperations
from hardsurface_addon.core.algorithms.inset_ops import InsetOperations

class TestAlgorithms(unittest.TestCase):
    """Test cases for Inset and Extrude algorithm logic."""
    
    def test_find_face_islands_disconnected(self):
        """Test finding face islands on completely disconnected faces."""
        rng = Randomization(10)
        extrude_ops = ExtrusionOperations(rng)
        
        # Mock 3 faces that don't share any edges
        face1 = MagicMock()
        face1.edges = []
        
        face2 = MagicMock()
        face2.edges = []
        
        face3 = MagicMock()
        face3.edges = []
        
        faces = [face1, face2, face3]
        islands = extrude_ops.find_face_islands(faces)
        
        # Since they are disconnected, we should get 3 separate islands of 1 face each
        self.assertEqual(len(islands), 3)
        self.assertEqual(len(islands[0]), 1)
        self.assertEqual(len(islands[1]), 1)
        self.assertEqual(len(islands[2]), 1)

    def test_find_face_islands_connected(self):
        """Test finding face islands on connected faces."""
        rng = Randomization(10)
        extrude_ops = ExtrusionOperations(rng)
        
        # Mock faces and shared edges
        face1 = MagicMock(name="Face1")
        face2 = MagicMock(name="Face2")
        face3 = MagicMock(name="Face3") # Disconnected face
        
        edge = MagicMock(name="SharedEdge")
        edge.link_faces = [face1, face2]
        
        face1.edges = [edge]
        face2.edges = [edge]
        face3.edges = []
        
        faces = [face1, face2, face3]
        islands = extrude_ops.find_face_islands(faces)
        
        # We expect 2 islands:
        # Island 1: [face1, face2] (connected via shared edge)
        # Island 2: [face3] (disconnected)
        self.assertEqual(len(islands), 2)
        
        # Verify sizes of islands
        island_sizes = sorted([len(island) for island in islands])
        self.assertEqual(island_sizes, [1, 2])

    def test_safety_margin_clamping(self):
        """Test that insets clamp correctly when safety_margin is applied."""
        rng = Randomization(42)
        inset_ops = InsetOperations(rng)
        
        # Mock a face with edges of length 0.1
        face = MagicMock()
        edge = MagicMock()
        edge.calc_length.return_value = 0.1
        face.edges = [edge]
        
        # Mock BMeshUtils.inset_face to return a dummy face
        sys.modules['hardsurface_addon.utils.bmesh_utils'].BMeshUtils.inset_face = MagicMock(return_value="InsetFace")
        
        # With safety_margin=0.01 and edge=0.1, max_safe_inset is (0.1 * 0.5) - 0.01 = 0.04
        # Even if we request a huge inset (e.g. 0.5), it should be clamped to 0.04!
        bm = MagicMock()
        result = inset_ops.apply_random_inset(
            bm, face, inset_min=0.5, inset_max=0.5, probability=1.0, safety_margin=0.01
        )
        
        # Verify that BMeshUtils.inset_face was called with the clamped amount (0.04)
        from hardsurface_addon.utils.bmesh_utils import BMeshUtils
        BMeshUtils.inset_face.assert_called_once()
        args, kwargs = BMeshUtils.inset_face.call_args
        clamped_amount = args[2]
        self.assertAlmostEqual(clamped_amount, 0.04)
        self.assertEqual(result, "InsetFace")

if __name__ == '__main__':
    unittest.main()
