
import unittest

from ogtrans.translate import find_basename


class FindBasenameTests(unittest.TestCase):
    def test_find_basename(self):

        self.assertEqual(find_basename("foobar/baz/my long filename.graffle/data.plist"), "my long filename")
        self.assertEqual(find_basename("foobar/baz/short.graffle/data.plist"), "short")
        self.assertEqual(find_basename("foobar/baz/my long filename.graffle"), "my long filename")
        self.assertEqual(find_basename("foobar/baz/short.graffle"), "short")
        self.assertEqual(find_basename("just.graffle"), "just")
        self.assertEqual(find_basename("foobar/files.graffle/juhu/illustrations.graffle/data.plist"), "illustrations")
        self.assertEqual(find_basename("foobar/files.graffle/juhu/illustrations.graffle"), "illustrations")
