
import re
import unittest

from textwrap import dedent

rtf_pattern = re.compile(dedent(r'''
    \{\\rtf1\\ansi\\ansicpg1252\\cocoartf1561\\cocoasubrtf600
    \{\\fonttbl\\f0\\fnil\\fcharset0 HelveticaNeue;\}
    \{\\colortbl;\\red255\\green255\\blue255;\}
    \{\\\*\\expandedcolortbl;;\}
    \\pard\\tx560\\tx1120\\tx1680\\tx2240\\tx2800\\tx3360\\tx3920\\tx4480\\tx5040\\tx5600\\tx6160\\tx6720\\pardirnatural\\qc\\partightenfactor0

    \\f0\\fs32 \\cf0 (?P<contents>.+\})''').strip(), re.DOTALL)

rtf_string2 = re.compile(dedent(r"""
    \{\\rtf1\\ansi\\ansicpg1252\\cocoartf1561\\cocoasubrtf600
    \{\\fonttbl\\f0\\fnil\\fcharset0 HelveticaNeue;\}
    \{\\colortbl;\\red255\\green255\\blue255;\}
    \{\\\*\\expandedcolortbl;;\}
    \\pard\\tx560\\tx1120\\tx1680\\tx2240\\tx2800\\tx3360\\tx3920\\tx4480\\tx5040\\tx5600\\tx6160\\tx6720\\pardirnatural\\qc\\partightenfactor0

    \\f0\\fs32 \\cf0 (?P<contents>.+)
    }
    """))


def rtf2md(text):
    
    m = rtf_pattern.match(text.strip())
    if m is None:
        raise Exception("no content found %s" % text)
    else:
        return m['contents']


class BasicTests(unittest.TestCase):
    """
    parse a pretty simple example
    """
 
    def test_simple_example(self):
        """

        """

        text = dedent(r"""
            {\rtf1\ansi\ansicpg1252\cocoartf1561\cocoasubrtf600
            {\fonttbl\f0\fnil\fcharset0 HelveticaNeue;}
            {\colortbl;\red255\green255\blue255;}
            {\*\expandedcolortbl;;}
            \pard\tx560\tx1120\tx1680\tx2240\tx2800\tx3360\tx3920\tx4480\tx5040\tx5600\tx6160\tx6720\pardirnatural\qc\partightenfactor0

            \f0\fs32 \cf0 This is some
            \b styled
            \b0  text}
        """)
        atext = dedent("""foo bar 
            bar
        """)
        self.failUnlessEqual(rtf2md(text), "This is some **styled** text.")


if __name__ == "__main__":
    unittest.main()
