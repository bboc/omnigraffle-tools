# -*- coding: utf-8 -*-

import argparse
from .path import Path
from .document import PlistWalker, PlistTextExtractor, PlistWriteTester


def cmd_extract(args):
    print("extract - text")
    pw = PlistTextExtractor(args.document)
    for canvas in pw.doc['Sheets']:
        pw.path = Path(canvas['SheetTitle'])
        pw.walk_plist(canvas)
        pw.process()


def cmd_inject(args):
    print("inject - not implemented")


def cmd_dump(args):
    print("dump file as text")
    pw = PlistWalker(args.document, verbose=True)
    pw.walk_plist(pw.doc)


def cmd_replace(args):
    print("test: replace text and write back ")

    pw = PlistWriteTester(args.document)
    pw.walk_plist(pw.doc)
    pw.process()


def main():

    # create the top-level parser
    parser = argparse.ArgumentParser(prog='ogtranslate')
    parser.add_argument('document', help='the OmniGraffle document (or the plist inside it')
    subparsers = parser.add_subparsers(help='sub-command help')

    p_extract = subparsers.add_parser('extract', help='extract text from OmniGraffle document')
    p_extract.add_argument('target', help='target file')
    p_extract.set_defaults(func=cmd_extract)
    p_inject = subparsers.add_parser('inject', help='inject text into OmniGraffle document')
    p_inject.add_argument('text_source', help='text file')
    p_inject.set_defaults(func=cmd_inject)

    p_dump = subparsers.add_parser('dump', help='dump text into OmniGraffle document')
    p_dump.set_defaults(func=cmd_dump)

    p_replace = subparsers.add_parser('replace', help='replace text and write back')
    p_replace.set_defaults(func=cmd_replace)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
