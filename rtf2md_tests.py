
import re
import unittest

from textwrap import dedent


# TODO: make this independent from fonts and colors
rtf_pattern = re.compile(dedent(r'''
    \{\\rtf1\\ansi\\ansicpg1252\\cocoartf1561\\cocoasubrtf600
    \{\\fonttbl\\f0\\fnil\\fcharset0 HelveticaNeue;\}
    \{\\colortbl;\\red255\\green255\\blue255;\}
    \{\\\*\\expandedcolortbl;;\}
    \\pard\\tx560\\tx1120\\tx1680\\tx2240\\tx2800\\tx3360\\tx3920\\tx4480\\tx5040\\tx5600\\tx6160\\tx6720\\pardirnatural\\qc\\partightenfactor0

    \\f0\\fs32 \\cf0 (?P<contents>.+)\}''').strip(), re.DOTALL)


bold_pattern = re.compile(r'\\b\s+(?P<styled_text>.+?)\s+\\b0', re.DOTALL)
italic_pattern = re.compile(r'\\i\s+(?P<styled_text>.+?)\s+\\i0', re.DOTALL)
newline_in_sentences = re.compile(r'(?P<char>\w)\n')
double_space_before_word = re.compile(r'\s\s(?P<char>\w)')
double_space_after_word = re.compile(r'(?P<char>\w)\s\s')

replacements = (

    (bold_pattern, '**\g<styled_text>**'),
    (italic_pattern, '**\g<styled_text>**'),
    (newline_in_sentences, '\g<char> '),
    (double_space_before_word, ' \g<char>'),
    (double_space_after_word, '\g<char> '),
)


def rtf2md(text):

    m = rtf_pattern.match(text.strip())
    if m is None:
        raise Exception("no content found %s" % text)
    else:
        result = m['contents']
        for pattern, repl in replacements:
            result = pattern.sub(repl, result, re.DOTALL)
        return result


class BasicTests(unittest.TestCase):
    """
    parse a pretty simple example
    """
    def test_plain_text(self):
        """
        Plain text should be extracted.
        """
        text = dedent(r"""
            {\rtf1\ansi\ansicpg1252\cocoartf1561\cocoasubrtf600
            {\fonttbl\f0\fnil\fcharset0 HelveticaNeue;}
            {\colortbl;\red255\green255\blue255;}
            {\*\expandedcolortbl;;}
            \pard\tx560\tx1120\tx1680\tx2240\tx2800\tx3360\tx3920\tx4480\tx5040\tx5600\tx6160\tx6720\pardirnatural\qc\partightenfactor0

            \f0\fs32 \cf0 some plain text}""")

        expected = 'some plain text'
        self.assertEqual(rtf2md(text), expected)

    def test_bold_text(self):
        """
        A some simple bold text should be converted to Markdown.
        """

        text = dedent(r"""
            {\rtf1\ansi\ansicpg1252\cocoartf1561\cocoasubrtf600
            {\fonttbl\f0\fnil\fcharset0 HelveticaNeue;}
            {\colortbl;\red255\green255\blue255;}
            {\*\expandedcolortbl;;}
            \pard\tx560\tx1120\tx1680\tx2240\tx2800\tx3360\tx3920\tx4480\tx5040\tx5600\tx6160\tx6720\pardirnatural\qc\partightenfactor0

            \f0\fs32 \cf0 This is some
            \b bold
            \b0  text}
        """)
        self.assertEqual(rtf2md(text), "This is some **bold** text")

    def test_italic_text(self):
        """
        A some simple bold text should be converted to Markdown.
        """

        text = dedent(r"""
            {\rtf1\ansi\ansicpg1252\cocoartf1561\cocoasubrtf600
            {\fonttbl\f0\fnil\fcharset0 HelveticaNeue;}
            {\colortbl;\red255\green255\blue255;}
            {\*\expandedcolortbl;;}
            \pard\tx560\tx1120\tx1680\tx2240\tx2800\tx3360\tx3920\tx4480\tx5040\tx5600\tx6160\tx6720\pardirnatural\qc\partightenfactor0

            \f0\fs32 \cf0 This is some
            \i italic
            \i0  text}
        """)
        self.assertEqual(rtf2md(text), "This is some **italic** text")


class MoreTests(unittest.TestCase):

    def test_combined_markup(self):
        """
        …
        """
        text = dedent(r"""{\rtf1\ansi\ansicpg1252\cocoartf1561\cocoasubrtf600
            {\fonttbl\f0\fnil\fcharset0 HelveticaNeue;}
            {\colortbl;\red255\green255\blue255;}
            {\*\expandedcolortbl;;}
            \pard\tx560\tx1120\tx1680\tx2240\tx2800\tx3360\tx3920\tx4480\tx5040\tx5600\tx6160\tx6720\pardirnatural\qc\partightenfactor0

            \f0\fs32 \cf0 Box with some
            \b bold
            \b0  and some
            \i italic
            \i0  text.\
            And a second paragraph}""")

        expected = 'foo'
        self.assertEqual(rtf2md(text), expected)

    def test_list_markup(self):
        """
        …
        """
        text = dedent(r"""{\rtf1\ansi\ansicpg1252\cocoartf1561\cocoasubrtf600
            {\fonttbl\f0\fnil\fcharset0 HelveticaNeue;\f1\fnil\fcharset0 LucidaGrande;}
            {\colortbl;\red255\green255\blue255;}
            {\*\expandedcolortbl;;}
            {\*\listtable{\list\listtemplateid1\listhybrid{\listlevel\levelnfc23\levelnfcn23\leveljc0\leveljcn0\levelfollow0\levelstartat1\levelspace360\levelindent0{\*\levelmarker \{square\}}{\leveltext\leveltemplateid1\'01\uc0\u9642 ;}{\levelnumbers;}\fi-360\li720\lin720 }{\listname ;}\listid1}}
            {\*\listoverridetable{\listoverride\listid1\listoverridecount0\ls1}}
            \pard\tx220\tx720\tx1120\tx1680\tx2240\tx2800\tx3360\tx3920\tx4480\tx5040\tx5600\tx6160\tx6720\li720\fi-720\pardirnatural\qc\partightenfactor0
            \ls1\ilvl0
            \f0\fs32 \cf0 {\listtext
            \f1 \uc0\u9642
            \f0     }list item\
            {\listtext
            \f1 \uc0\u9642
            \f0     }and another one\
            }""")

        expected = 'foo'
        self.assertEqual(rtf2md(text), expected)



if __name__ == "__main__":
    unittest.main()
