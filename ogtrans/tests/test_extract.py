from argparse import Namespace
import logging
import os
import tempfile
import unittest

from ogtrans.commands import OmniGraffleTranslator


class ExtractTranslationsTests(unittest.TestCase):

    def setUp(self):
        self.test_data = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test-data')
        self.tmp_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tmp')
        if not os.path.exists(self.tmp_path):
            os.makedirs(self.tmp_path)
        logging.basicConfig(level=logging.DEBUG)

    def test_extract_translations(self):
        """
        Extract translations
        """
        tmpfolder = tempfile.TemporaryDirectory(dir=self.tmp_path)

        args = Namespace(canvas=None,
                         func=OmniGraffleTranslator.cmd_extract_translations,
                         loglevel=30,
                         source=os.path.join(self.test_data, 'rtfprocessor-tests.graffle'),
                         target=tmpfolder.name)

        tr = OmniGraffleTranslator(args)
        tr.args.func(tr)
        translations = os.path.join(tmpfolder.name, 'rtfprocessor-tests')
        self.assertTrue(os.path.exists(translations))
        self.assertTrue(os.path.exists(os.path.join(translations, 'rtfprocessor-tests.pot')))
        self.assertTrue(os.path.exists(os.path.join(translations, 'textbox-a.md')))
