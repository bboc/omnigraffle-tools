# -*- coding: utf-8 -*-

import argparse
from lxml import etree as ET
from textwrap import dedent
import plistlib

from .rtf2md import rtf2md
from .rtf_processor import split_rtf

substitute = dedent(r"""{\rtf1\ansi\ansicpg1252\cocoartf1561\cocoasubrtf600
{\fonttbl\f0\fnil\fcharset0 HelveticaNeue;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\pard\tx560\tx1120\tx1680\tx2240\tx2800\tx3360\tx3920\tx4480\tx5040\tx5600\tx6160\tx6720\pardirnatural\qc\partightenfactor0

\f0\fs32 \cf0 Replaced text}""")


def replace_text_in_element(element):
    element[1].text = substitute


def dump_element(element):
    raw_rtf = element[1].text
    print('-' * 30)
    print(raw_rtf)
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
    print("extract - text")
    pw = PlistTextExtractor(args.document)
    pw.process()


def cmd_inject(args):
    print("inject - not implemented")


def cmd_dump(args):
    print("dump file as text")
    pw = PlistWalker(args.document, verbose=True)


def cmd_replace(args):
    print("test: replace text and write back ")

    tree = ET.parse(args.document)
    root = tree.getroot()

    for element in root.findall(".//dict//key/.."):
        if element[0].text == "Text":
            replace_text_in_element(element)
    tree.write('output.graffle', encoding="UTF-8", xml_declaration=True)


class PlistWalker(object):

    def __init__(self, filename, verbose=False):
        self.verbose = verbose
        self._path = []
        fp = open(filename, 'rb')
        doc = plistlib.load(fp, fmt=plistlib.FMT_XML)

        self.walk_plist(doc)

    def walk_plist(self, current, level=0, name=''):
        def tabbed(*args):
            if self.verbose:
                print(level * '  ', *args)

        def node_value(item):
            if type(item) == bytes:
                return '<bytes>'
            elif type(item) == str:
                if item.startswith(r'{\rtf'):
                    return 'RTF-TEXT'
            return item

        # do whatever with this item...
        self.selector(current)

        if type(current) == list:
            tabbed('%s [' % name)
            for idx, item in enumerate(current):
                self._path.append('[%s]' % idx)
                self.walk_plist(item, level + 1)
                self._path.pop()
            tabbed(']')
        elif type(current) == dict:
            tabbed('%s {' % name)
            for key, item in current.items():
                self._path.append('.%s' % key)
                self.walk_plist(item, level + 1, key)
                self._path.pop()
            tabbed('}')
        else:
            value = node_value(current)
            tabbed(name, ':', node_value(current))
            if value == 'RTF-TEXT':
                tabbed(self.path)

    @property
    def path(self):
        return ''.join(self._path)

    def selector(self, item):
        """Do whatever with any item that is traversed."""
        pass


class PlistTextExtractor(PlistWalker):

    GRAPHICS_CLASSES = [
        # 'Group',
        'LineGraphic',
        'ShapedGraphic',
        # 'TableGroup',
    ]

    def __init__(self, filename):
        self.text_containers = []
        super().__init__(filename)

    def selector(self, current):
        if self.is_text_container(current) and self.has_text(current):
            self.text_containers.append(current)

    def is_text_container(self, current):
        return type(current) == dict and 'Class' in current and current['Class'] in self.GRAPHICS_CLASSES

    def has_text(self, current):

        try:
            text = current['Text']['Text']
        except KeyError:
            return False

        if text.startswith(r'{\rtf'):
            return True
        else:
            return False

    def process(self):
        for item in self.text_containers:
            print('-' * 30)
            raw_rtf = item['Text']['Text']
            contents = split_rtf(raw_rtf)['contents']
            print(rtf2md(contents))


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
