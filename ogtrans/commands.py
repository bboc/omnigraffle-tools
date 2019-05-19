# -*- coding: utf-8 -*-

import argparse
import logging
import os
import plistlib
from textwrap import dedent

from .path import Path
from .document import PlistWalker, PlistTextExtractor
from .translate import find_basename, NewTranslationMemory, TranslationMemoryFile

"""
Translation of Omnigrafle files

1. Create Translation memory
    - get all cavases in file
    - for each canvas: get all text objects and dump to pot-file

2. Update translatiosn
    - create a copy of OmniGraffle source file language suffix
    - read po-file and make a translation dictionary d[msgid] = msgstr
        (replace newlines and quotes!!)
    - walk through all objects, if text: replace with translated text
    - save

TODO: how to make sure OmniGraffle files are not changed between exporting pot and translation?
    Create dedicated image repo (needs branchens for each resource release) or add to the repo
     where illustrations are used (adds lots of duplication)

Do we need keys and template files?

    - create a key (hash) for each text
    - create a omnigraffle template file where texts are replaced by hashes
    - copy templates and fill in translations template files
"""

class OmniGraffleTranslator(object):

    def __init__(self, args=None):
        """Read args from commandline if not present."""
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
            # TODO: add filter for single canvas here
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
        """
        Inject translations from po-files into OmniGraffle document(s).

        If any of the parameters is a directory, actual filenames will be
        inferred from source file, if source is a directory, all OmniGraffle
        documents in that folder will be processed.
        """
        print("translate document - not implemented")
        # TODO: check if target == source

        if not os.path.exists(self.args.source):
            logging.error("source '%s' does not exist", self.args.source)
            return

        if os.path.isdir(self.args.source):
            for filename in sorted(os.listdir(self.args.source)):
                if filename.endswith(".graffle"):
                    self.translate_document(os.path.join(self.args.source, filename),
                                            self.args.target,
                                            self.args.translations)
        else:
            self.translate_document(self.args.source, self.args.target, self.args.translations)

    def translate_document(self, source, target, translations):
        """Create a copy of an OmniGraffle document and then translate it."""
        self.open_copy_of_document(source, target=target)
        if os.path.isdir(translations):
            tm_file = os.path.join(translations, os.path.splitext(os.path.basename(source))[0] + '.po')
        else:
            tm_file = translations
        tm = self.read_translation_memory(tm_file)


        for canvas in self.doc.canvases():
            c = Canvas(canvas)
            c.walk(partial(inject_translations, tm))

        self.og.windows.first().save()

    def open_copy_of_document(self, source, target=None, suffix=None):
        """
        Create and open a copy of an omnigraffle document.
        Target takes precedence over sufix, if target is given and is a directory, the target
        file name will be created from target and the basename of source. If target is ommited,
        but suffix is given, the target filename will be created by extending source with suffix.
        """
        if target:
            if os.path.isdir(target):
                # create full target file name from basenam of source file
                target = os.path.join(target, os.path.basename(source))
        if suffix and not target:
            root, ext = os.path.splitext(source)
            target = root + '-' + suffix + ext
        print("copy:", source, target)
        shutil.copyfile(source, target)
        self.open_document(target)


    def cmd_dump(self):
        print("dump file as text")
        pw = PlistWalker(self.args.source, verbose=True)
        pw.walk_plist(pw.doc)

    def cmd_replace(self):
        print("test: replace text and write back ")

        pw = PlistWriteTester(self.args.source)
        pw.walk_plist(pw.doc)

        SUBSTITUTE = dedent(r"""
                {\rtf1\ansi\ansicpg1252\cocoartf1561\cocoasubrtf600
                {\fonttbl\f0\fnil\fcharset0 HelveticaNeue;}
                {\colortbl;\red255\green255\blue255;}
                {\*\expandedcolortbl;;}
                \pard\tx560\tx1120\tx1680\tx2240\tx2800\tx3360\tx3920\tx4480\tx5040\tx5600\tx6160\tx6720\pardirnatural\qc\partightenfactor0

                \f0\fs32 \cf0 Replaced text}""").strip()

        for item in pw.translatables:
            item.raw_text = SUBSTITUTE

        fp = open('out.graffle', 'wb')
        plistlib.dump(self.doc, fp, fmt=plistlib.FMT_XML, sort_keys=True, skipkeys=False)

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
                                         description="Translate canvases in OmniGraffle Documents",
                                         epilog="Documents must be uncrompressed flat files.")

        subparsers = parser.add_subparsers()
        OmniGraffleTranslator.cmd_extract_subparser(subparsers)
        OmniGraffleTranslator.cmd_dump_subparser(subparsers)
        OmniGraffleTranslator.cmd_translate_subparser(subparsers)
        return parser

    @staticmethod
    def cmd_extract_subparser(subparsers):
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
    def cmd_dump_subparser(subparsers):
        sp = subparsers.add_parser('dump',
                                   help="Dump file structure")
        sp.add_argument('source', type=str,
                        help='an OmniGraffle file')
        OmniGraffleTranslator.add_verbose(sp)
        sp.set_defaults(func=OmniGraffleTranslator.cmd_dump)

    @staticmethod
    def cmd_translate_subparser(subparsers):
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
                        help='a po-file or a folder that contains PO file and potentially other files')
        # sp.add_argument('language', type=str,
        #                 help='two-digit language identifier')
        OmniGraffleTranslator.add_verbose(sp)
        sp.set_defaults(func=OmniGraffleTranslator.cmd_translate)


def main():
    translator = OmniGraffleTranslator()
    print(repr(translator.args))
    translator.args.func(translator)


if __name__ == "__main__":
    main()

