
import unittest
from rtf2md import rtf2md

from textwrap import dedent


class BasicTests(unittest.TestCase):
    def test_plain_text(self):
        """Plain text should be extracted correctly."""
        text = r'\f0\fs32 \cf0 some plain text'

        expected = 'some plain text'
        self.assertEqual(rtf2md(text), expected)

    def test_bold_text(self):
        """A some simple bold text should be converted to Markdown."""
        text = dedent(r"""
            \f0\fs32 \cf0 This is some
            \b bold
            \b0  text
        """)
        self.assertEqual(rtf2md(text), "This is some **bold** text")

    def test_italic_text(self):
        """A some simple italic text should be converted to Markdown."""
        text = dedent(r"""
            \f0\fs32 \cf0 This is some
            \i italic
            \i0  text
        """)
        self.assertEqual(rtf2md(text), "This is some _italic_ text")


class MoreTests(unittest.TestCase):

    def test_combined_markup(self):
        """Italics and bold at the same time are properly processed."""
        text = dedent(r"""
            \f0\fs32 \cf0 Box with some
            \b bold
            \b0  and some
            \i italic
            \i0  text.\
            And a second paragraph""")

        expected = dedent("""\
            Box with some **bold** and some _italic_ text.
            And a second paragraph""")
        self.assertEqual(rtf2md(text), expected)

    def test_list_markup(self):
        """
        …
        """
        text = dedent(r"""
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
