"""
HardSurface Pro Test Runner.

Usage:
    cd /Users/bensaadmohammed/Documents/PluginBlender
    python -m hardsurface_addon.tests.run_tests

Or from Blender script editor:
    exec(open("/Users/bensaadmohammed/Documents/PluginBlender/hardsurface_addon/tests/run_tests.py").read())
"""

#!/usr/bin/env python3
"""
HardSurface Pro Test Runner.

Usage:
    cd /Users/bensaadmohammed/Documents/PluginBlender
    python3 -m hardsurface_addon.tests.run_tests

Or from Blender script editor:
    exec(open("/Users/bensaadmohammed/Documents/PluginBlender/hardsurface_addon/tests/run_tests.py").read())
"""

import sys
import os
from unittest.mock import MagicMock

# =============================================================================
# CRITICAL: Inject mock modules BEFORE any addon import
# =============================================================================
sys.modules['bpy'] = MagicMock()
sys.modules['bpy.types'] = MagicMock()
sys.modules['bpy.props'] = MagicMock()
sys.modules['bmesh'] = MagicMock()
sys.modules['bmesh.types'] = MagicMock()
sys.modules['bmesh.ops'] = MagicMock()
sys.modules['mathutils'] = MagicMock()
sys.modules['mathutils.Vector'] = MagicMock()
sys.modules['mathutils.Matrix'] = MagicMock()

# Add parent directory to path for imports
addon_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if addon_dir not in sys.path:
    sys.path.insert(0, addon_dir)

# Now safe to import unittest
import unittest

def run_tests():
    """Discover and run all tests."""
    loader = unittest.TestLoader()
    tests_dir = os.path.dirname(os.path.abspath(__file__))
    suite = loader.discover(tests_dir, pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print(f"\n{'='*70}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    print(f"{'='*70}")
    
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
