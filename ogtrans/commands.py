# -*- coding: utf-8 -*-

import argparse
import logging
import os
from textwrap import dedent

from .path import Path
from .document import PlistWalker, PlistTextExtractor, PlistWriteTester
from .translate import find_basename, NewTranslationMemory


class OmniGraffleTranslator(object):

    def __init__(self, args=None):
        """Read args from commandline if not present, and connect to OmniGraffle app."""
        if args:
            self.args = args
        else:
            self.args = self.parse_commandline()

        self._check_args()
        self.doc = None

    def _check_args(self):
        """Hook to validate commandline arguments."""
        pass

    def cmd_extract_translations(self):
        """
        Extract text from args.source and write to a subfolder of args.target
        with the name of the omnigraffle file.
        """
        print("extract - text")

        # find all translatable text
        pw = PlistTextExtractor(self.args.source)
        for canvas in pw.doc['Sheets']:
            pw.path = Path(canvas['SheetTitle'])
            pw.walk_plist(canvas)

        basename = find_basename(self.args.source)
        outdir = os.path.join(self.args.target, basename)
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        tm = NewTranslationMemory()
        for item in pw.translatables:
            if item.destination:
                fp = open(os.path.join(outdir, '%s.md' % item.destination), 'w+')
                fp.write(item.rtf.markdown)
                fp.close()
                # dump markdown to file
            else:
                tm.add(item.rtf.markdown, item.context)
        tm.dump_translation_memory(os.path.join(outdir, basename))

    def cmd_translate(self):
        print("translate document - not implemented")

    def cmd_dump(self):
        print("dump file as text")
        pw = PlistWalker(self.args.source, verbose=True)
        pw.walk_plist(pw.doc)

    def cmd_replace(self):
        print("test: replace text and write back ")

        pw = PlistWriteTester(self.args.source)
        pw.walk_plist(pw.doc)
        pw.process()

    def parse_commandline(self):
        """Parse commandline, do some checks and return args."""

        parser = self.get_parser()
        args = parser.parse_args()
        # set up loglevel
        logging.basicConfig(level=args.loglevel)
        return args

    @staticmethod
    def add_verbose(parser):
        parser.add_argument(
            '-d', '--debug',
            help="print debug output",
            action="store_const", dest="loglevel", const=logging.DEBUG,
            default=logging.WARNING
        )
        parser.add_argument(
            '-v', '--verbose',
            help="more detailed output",
            action="store_const", dest="loglevel", const=logging.INFO,
        )

    @staticmethod
    def get_parser():
        parser = argparse.ArgumentParser(fromfile_prefix_chars='@',
                                         description="Translate canvases in OmniGraffle 6.",
                                         epilog="If a file fails, simply try again.")

        subparsers = parser.add_subparsers()
        OmniGraffleTranslator.add_parser_extract(subparsers)
        OmniGraffleTranslator.add_parser_list(subparsers)
        OmniGraffleTranslator.add_parser_translate(subparsers)
        return parser

    @staticmethod
    def add_parser_extract(subparsers):
        sp = subparsers.add_parser('extract',
                                   help="Extract a POT file from an Omnigraffle document.")
        sp.add_argument('source', type=str,
                        help='an OmniGraffle file')
        sp.add_argument('target', type=str,
                        help='target folder')
        sp.add_argument('--canvas', type=str,
                        help='translate canvas with given name')
        OmniGraffleTranslator.add_verbose(sp)
        sp.set_defaults(func=OmniGraffleTranslator.cmd_extract_translations)

    @staticmethod
    def add_parser_list(subparsers):
        sp = subparsers.add_parser('dump',
                                   help="Dump file structure")
        sp.add_argument('source', type=str,
                        help='an OmniGraffle file')
        OmniGraffleTranslator.add_verbose(sp)
        sp.set_defaults(func=OmniGraffleTranslator.cmd_dump)

    @staticmethod
    def add_parser_translate(subparsers):
        sp = subparsers.add_parser('translate',
                                   description=dedent("""Translate an Omnigraffle document(s) using po-files.

                                        If any of the parameters is a directory, actual filenames will be
                                        inferred from source file, if source is a directory, all OmniGraffle
                                        documents in that folder will be processed.
                                        Example:

                                           ogtranslate translate graffle/src/ graffle/de/ text/de/

                                        will create translated copies from each document found in graffle/src
                                        in graffle/de, using a separate po-file for each document, located
                                        in graffle/de.

                                            ogtranslate translate graffle/src/ graffle/de/ text/de/all.po

                                        will create translated copies from each document found in graffle/src
                                        in graffle/de, using text/de/all.po for translating each document."""))
        sp.add_argument('source', type=str,
                        help='an OmniGraffle document or a folder')
        sp.add_argument('target', type=str,
                        help='target filename or folder')
        sp.add_argument('translations', type=str,
                        help='a po-file or a folder')
        # sp.add_argument('language', type=str,
        #                 help='two-digit language identifier')
        OmniGraffleTranslator.add_verbose(sp)
        sp.set_defaults(func=OmniGraffleTranslator.cmd_translate)


def main():
    translator = OmniGraffleTranslator()
    translator.args.func(translator)


if __name__ == "__main__":
    main()

