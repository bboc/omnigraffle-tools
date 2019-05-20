
import unittest
from ogtrans.rtf_processor import split_rtf

from textwrap import dedent


class BasicTests(unittest.TestCase):
    def test_plain_text(self):
        """A simple example should be split properly."""
        text = dedent(r"""
            {\rtf1\ansi\ansicpg1252\cocoartf1561\cocoasubrtf600
            {\fonttbl\f0\fnil\fcharset0 HelveticaNeue;}
            {\colortbl;\red255\green255\blue255;}
            {\*\expandedcolortbl;;}
            \pard\tx560\tx1120\tx1680\tx2240\tx2800\tx3360\tx3920\tx4480\tx5040\tx5600\tx6160\tx6720\pardirnatural\qc\partightenfactor0

            \f0\fs32 \cf0 some plain text}""")

        expected = dict(header=dedent(r"""
                            {\rtf1\ansi\ansicpg1252\cocoartf1561\cocoasubrtf600
                            {\fonttbl\f0\fnil\fcharset0 HelveticaNeue;}
                            {\colortbl;\red255\green255\blue255;}
                            {\*\expandedcolortbl;;}
                            \pard\tx560\tx1120\tx1680\tx2240\tx2800\tx3360\tx3920\tx4480\tx5040\tx5600\tx6160\tx6720\pardirnatural\qc\partightenfactor0""").strip(),
                        contents=r'\f0\fs32 \cf0 some plain text',
                        fonts={'0': 'HelveticaNeue'},
                        content_prefix=r'\f0\fs32 \cf0')
        result = split_rtf(text)

        self.assertEqual(result['header'], expected['header'])
        self.assertEqual(result['contents'], expected['contents'])
        self.assertEqual(result['fonts'], expected['fonts'])
        self.assertEqual(result['content_prefix'], expected['content_prefix'])

        # fail on new elements that haven't been tested above!
        self.assertEqual(result, expected)

    def test_list_markup(self):
        """
        …
        """
        text = dedent(r"""
            {\rtf1\ansi\ansicpg1252\cocoartf1561\cocoasubrtf600
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

        expected = dict(header=dedent(r"""
                            {\rtf1\ansi\ansicpg1252\cocoartf1561\cocoasubrtf600
                            {\fonttbl\f0\fnil\fcharset0 HelveticaNeue;\f1\fnil\fcharset0 LucidaGrande;}
                            {\colortbl;\red255\green255\blue255;}
                            {\*\expandedcolortbl;;}
                            {\*\listtable{\list\listtemplateid1\listhybrid{\listlevel\levelnfc23\levelnfcn23\leveljc0\leveljcn0\levelfollow0\levelstartat1\levelspace360\levelindent0{\*\levelmarker \{square\}}{\leveltext\leveltemplateid1\'01\uc0\u9642 ;}{\levelnumbers;}\fi-360\li720\lin720 }{\listname ;}\listid1}}
                            {\*\listoverridetable{\listoverride\listid1\listoverridecount0\ls1}}
                            \pard\tx220\tx720\tx1120\tx1680\tx2240\tx2800\tx3360\tx3920\tx4480\tx5040\tx5600\tx6160\tx6720\li720\fi-720\pardirnatural\qc\partightenfactor0""").strip(),
                        contents=dedent(r"""
                            \ls1\ilvl0
                            \f0\fs32 \cf0 {\listtext
                            \f1 \uc0\u9642
                            \f0     }list item\
                            {\listtext
                            \f1 \uc0\u9642
                            \f0     }and another one\
                            """).strip(),
                        fonts={'0': 'HelveticaNeue', '1': 'LucidaGrande'},
                        content_prefix='')
        result = split_rtf(text)

        self.assertEqual(result['header'], expected['header'])
        self.assertEqual(result['contents'], expected['contents'])
        self.assertEqual(result['fonts'], expected['fonts'])
        # fail on new elements that haven't been tested above!
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
