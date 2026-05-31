import sys
import os
import unittest

# Add parent directory to path for absolute imports
addon_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if addon_dir not in sys.path:
    sys.path.insert(0, addon_dir)


class TestDisplaceModulesExist(unittest.TestCase):
    """Verify displace operator and panel source files exist."""

    def test_noise_displace_file_exists(self):
        """Noise displace operator file must exist."""
        path = os.path.join(addon_dir, 'operators', 'displace', 'op_noise_displace.py')
        self.assertTrue(os.path.isfile(path))

    def test_image_displace_file_exists(self):
        """Image displace operator file must exist."""
        path = os.path.join(addon_dir, 'operators', 'displace', 'op_image_displace.py')
        self.assertTrue(os.path.isfile(path))

    def test_displace_panel_file_exists(self):
        """Displace panel file must exist."""
        path = os.path.join(addon_dir, 'ui', 'panels', 'displace_panel.py')
        self.assertTrue(os.path.isfile(path))


class TestDisplaceSourceContent(unittest.TestCase):
    """Inspect source files for expected identifiers without importing Blender modules."""

    def _read_file(self, *parts):
        path = os.path.join(addon_dir, *parts)
        with open(path, 'r') as f:
            return f.read()

    def test_noise_displace_has_bl_idname(self):
        """Noise displace operator must define correct bl_idname."""
        src = self._read_file('operators', 'displace', 'op_noise_displace.py')
        self.assertIn('bl_idname = "hardsurface.noise_displace"', src)

    def test_noise_displace_has_bl_label(self):
        """Noise displace operator must define correct bl_label."""
        src = self._read_file('operators', 'displace', 'op_noise_displace.py')
        self.assertIn('bl_label = "Noise Displace"', src)

    def test_noise_displace_has_execute(self):
        """Noise displace operator must define execute method."""
        src = self._read_file('operators', 'displace', 'op_noise_displace.py')
        self.assertIn('def execute(self, context):', src)

    def test_noise_displace_has_poll(self):
        """Noise displace operator must define poll method."""
        src = self._read_file('operators', 'displace', 'op_noise_displace.py')
        self.assertIn('def poll(cls, context):', src)

    def test_image_displace_has_bl_idname(self):
        """Image displace operator must define correct bl_idname."""
        src = self._read_file('operators', 'displace', 'op_image_displace.py')
        self.assertIn('bl_idname = "hardsurface.image_displace"', src)

    def test_image_displace_has_bl_label(self):
        """Image displace operator must define correct bl_label."""
        src = self._read_file('operators', 'displace', 'op_image_displace.py')
        self.assertIn('bl_label = "Image Displace"', src)

    def test_image_displace_has_execute(self):
        """Image displace operator must define execute method."""
        src = self._read_file('operators', 'displace', 'op_image_displace.py')
        self.assertIn('def execute(self, context):', src)

    def test_image_displace_has_poll(self):
        """Image displace operator must define poll method."""
        src = self._read_file('operators', 'displace', 'op_image_displace.py')
        self.assertIn('def poll(cls, context):', src)

    def test_image_displace_has_invoke(self):
        """Image displace operator must define invoke method to load props."""
        src = self._read_file('operators', 'displace', 'op_image_displace.py')
        self.assertIn('def invoke(self, context, event):', src)
        self.assertIn('wm.image_displace_props', src)

    def test_image_displace_saves_props(self):
        """Image displace execute must save props back to window manager."""
        src = self._read_file('operators', 'displace', 'op_image_displace.py')
        self.assertIn('wm = context.window_manager', src)
        self.assertIn("props.image_path = self.image_path", src)

    def test_panel_has_correct_id(self):
        """Displace panel must define correct bl_idname."""
        src = self._read_file('ui', 'panels', 'displace_panel.py')
        self.assertIn('bl_idname = "VIEW3D_PT_hardsurface_displace"', src)

    def test_panel_references_both_operators(self):
        """Displace panel must reference both operators."""
        src = self._read_file('ui', 'panels', 'displace_panel.py')
        self.assertIn('hardsurface.noise_displace', src)
        self.assertIn('hardsurface.image_displace', src)

    def test_property_groups_in_operator_props(self):
        """Operator props file must contain NoiseDisplaceProps and ImageDisplaceProps."""
        src = self._read_file('properties', 'operator_props.py')
        self.assertIn('class NoiseDisplaceProps', src)
        self.assertIn('class ImageDisplaceProps', src)

    def test_registration_imports_displace(self):
        """Registration classes must import displace panel and operators."""
        src = self._read_file('registration', 'classes.py')
        self.assertIn('VIEW3D_PT_hardsurface_displace', src)
        self.assertIn('OBJECT_OT_noise_displace', src)
        self.assertIn('OBJECT_OT_image_displace', src)


if __name__ == '__main__':
    unittest.main()
