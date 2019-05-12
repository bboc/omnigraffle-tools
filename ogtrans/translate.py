# -*- coding: utf-8 -*-


import argparse
from lxml import etree as ET
from rtf2md_tests import rtf2md
from textwrap import dedent

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


def cmd_replace(args):
    print("test: replace text and write back ")

    tree = ET.parse(args.document)
    root = tree.getroot()

    for element in root.findall(".//dict//key/.."):
        if element[0].text == "Text":
            replace_text_in_element(element)
    tree.write('output.graffle', encoding="UTF-8", xml_declaration=True)


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
