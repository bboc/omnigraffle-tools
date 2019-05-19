# -*- coding: utf-8 -*-

import argparse
import logging
import os
import plistlib
import shutil
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
        pw.collect_translatables()
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
        print("translate document")
        # TODO: check if target == source (also: target is dir and same as dir of sourcefile)

        if not os.path.exists(self.args.source):
            logging.error("source '%s' does not exist", self.args.source)
            return

        # create target as directory if it does not exist
        # FIXME: target might be a file (ending in .graffle)
        if not os.path.exists(self.args.target):
            os.makedirs(self.args.target)

        if os.path.isdir(self.args.source):
            for filename in sorted(os.listdir(self.args.source)):
                if filename.endswith(".graffle"):
                    self.translate_document(os.path.join(self.args.source, filename),
                                            self.args.target,
                                            self.args.translations)
        else:
            self.translate_document(self.args.source, self.args.target, self.args.translations)

    def translate_document(self, source_filename, target, translations):
        """Translate an OmniGraffle document and save result to new location."""

        document_basename = find_basename(source_filename)
        # translations: file: open PO file
        #               folder: check if contains PO file with basename, open that
        #               otherwise: open subfolder/basename.po
        if os.path.isdir(translations):
            po_file_only = False
            for file in [os.path.join(translations, document_basename + '.po'),
                         os.path.join(translations, document_basename, document_basename + '.po')]:
                if os.path.exists(file):
                    tm_file = file
                    break
            else:
                raise Exception('po-file not found', translations, document_basename)
        else:
            po_file_only = True
            tm_file = translations
        tm = TranslationMemoryFile(tm_file)
        # open plist and extract translatables
        pw = PlistTextExtractor(source_filename)
        pw.collect_translatables()
        # go through translatables and translate using PO and md files (if present)
        # TODO: tl might be empty, what then?
        for item in pw.translatables:
            if item.destination and not po_file_only: 
                tl = self.get_translation_from_file(item.destination, translations, document_basename)
            else:
                tl = tm.translate(item.rtf.markdown)
                item.rtf.markdown = tl
            if tl:
                item.translate(tl)

        # find out what the new document's filename is (target is filename or directory?)
        # TODO: what about files that contain images??
        if target.endswith('.graffle') or target.endswith('.plist'):
            target_filename = target
        else:
            target_filename = os.path.join(target, '%s.%s' % (document_basename, 'graffle'))

        # then save result to new document
        fp = open(target_filename, 'wb')
        plistlib.dump(pw.doc, fp, fmt=plistlib.FMT_XML, sort_keys=True, skipkeys=False)

    def copy_document(self, source, target):
        """
        Create a copy of an omnigraffle document.

        If target is directory, create document with same basename, otherwise use target as
        document name.
        """
        # FIXME: this code is wrong
        if target:
            if os.path.isdir(target):
                # create full target file name from basenam of source file
                target = os.path.join(target, os.path.basename(source))
        if suffix and not target:
            root, ext = os.path.splitext(source)
            target = root + '-' + suffix + ext
        shutil.copy(source, new_filename)

    def get_translation_from_file(self, filename, directory, document_basename):
        """
        Read translations from <filename>.md file that is either in <directory>, or in
        subdirectory <basename>. Raise exception if file not found.
        """
        for file in [os.path.join(directory, filename + '.md'),
                     os.path.join(directory, document_basename, filename + '.md')]:
            print(file)
            if os.path.exists(file):
                with open(file, 'r') as fp:
                    return fp.read()
        raise Exception('file not found', filename, directory, document_basename)

    def cmd_dump(self):
        print("dump file as text")
        pw = PlistWalker(self.args.source, verbose=True)
        pw.walk_plist(pw.doc)

    def cmd_test(self):
        print("test: replace text and write back ")

        pw = PlistTextExtractor(self.args.source)
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
        plistlib.dump(pw.doc, fp, fmt=plistlib.FMT_XML, sort_keys=True, skipkeys=False)

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
        OmniGraffleTranslator.cmd_translate_subparser(subparsers)
        OmniGraffleTranslator.cmd_dump_subparser(subparsers)
        OmniGraffleTranslator.cmd_test_subparser(subparsers)
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

    def cmd_test_subparser(subparsers):
        sp = subparsers.add_parser('test',
                                   help="Run some test code")
        sp.add_argument('source', type=str,
                        help='an OmniGraffle file')
        OmniGraffleTranslator.add_verbose(sp)
        sp.set_defaults(func=OmniGraffleTranslator.cmd_test)

    @staticmethod
    def cmd_translate_subparser(subparsers):
        sp = subparsers.add_parser('translate',
                                   description=dedent("""Translate an Omnigraffle document(s) using po-files.

                                        If any of the parameters is a directory, actual filenames will be
                                        inferred from source file, if source is a directory, all OmniGraffle
                                        documents in that folder will be processed. If translation is a folder,
                                        ogrtrans will look for translations in that folder as well as in
                                        subfolders with each document's names.
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
