from argparse import Namespace
import logging
import os
import tempfile
import unittest

from ogtrans.commands import OmniGraffleTranslator


class TranslateTests(unittest.TestCase):

    def setUp(self):
        self.tmp_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tmp')
        if not os.path.exists(self.tmp_path):
            os.makedirs(self.tmp_path)
        logging.basicConfig(level=logging.DEBUG)

    def test_one_file(self):
        """
        One file with target pointing to one PO file should be correctly tranlsated.
        """
        self.fail("not implemented")
        tmpfolder = tempfile.TemporaryDirectory(dir=self.tmp_path)

        args = Namespace(canvas=None,
                         func=OmniGraffleTranslator.cmd_translate,
                         loglevel=30,
                         source='ogtrans/test-data/rtfprocessor-tests.graffle',
                         target=tmpfolder.name)

        tr = OmniGraffleTranslator(args)
        tr.args.func(tr)

    def test_po_and_markdown(self):
        """
        One file with target pointing to directory with PO and markdown file should be correctly tranlsated.
        """
        self.fail("not implemented")

    def test_multiple_files(self):
        """
        source: dir, target: dir.
        """
        self.fail("not implemented")

    def test_multiple_files_single_po(self):
        """
        source: dir, target: single po file
        """
        self.fail("not implemented")
