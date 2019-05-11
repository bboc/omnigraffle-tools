# -*- coding: utf-8 -*-


import argparse
from lxml import etree as ET
from rtf2md_tests import rtf2md


def dump_element(element):
    raw_rtf = element[1].text
    print('-' * 30)
    try:
        print(rtf2md(raw_rtf))
    except:
        print("error", raw_rtf)
    # get to the parents parent (which is the Object itself)
    parent = element.getparent()
    for idx, item in enumerate(parent):
        if item.text == "UserInfo":
            print(idx, item.text)


def print_unitest(element):
    """Extract marked up text from rtf and output as a unittest skeleton."""

    raw_rtf = element[1].text
    print('''
        def test_something(self):
            """
            …
            """
            text = dedent("""%(raw_rtf)s""")

            expected = 'foo'
            self.assertEqual(rtf2md(text), expected)

    ''' % dict(raw_rtf=raw_rtf))


def cmd_extract(args):
    print("extract - not implemented")


def cmd_inject(args):
    print("inject - not implemented")


def cmd_dump(args):
    print("dump text")

    tree = ET.parse(args.document)
    root = tree.getroot()

    for element in root.findall(".//dict//key/.."):
        # get all dicts where the text of the first elementsi "Text"
        # TODO: this is probably not very robust
        if element[0].text == "Text":
            dump_element(element)


if __name__ == "__main__":

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

    args = parser.parse_args()
    args.func(args)
