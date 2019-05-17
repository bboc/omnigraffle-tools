
import re

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

linebreaks_pattern = re.compile(r'(\\)\n', re.DOTALL)

# TODO: \\\n marks a line break in rtf all others can go
newline_in_sentences = re.compile(r'(?P<char>\w)\n')
# TODO: all double whitespace afte the first word character should go
double_space_before_word = re.compile(r'\s\s(?P<char>\w)')
double_space_after_word = re.compile(r'(?P<char>\w)\s\s')

replacements = (

    (bold_pattern, '**\g<styled_text>**'),
    (newline_in_sentences, '\g<char> '),
    (italic_pattern, '_\g<styled_text>_'),
    (linebreaks_pattern, '\n'),
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

# split text and control words on beginning of line that are not unicode strings
content_start = re.compile(r'^(?P<controlwords>((\\[^\su]\S*)\s)+)(?P<text>.*)')

header_markers = [
    r'{\rtf1',
    # r'{\fonttbl\f0\fnil\fcharset0 HelveticaNeue;\f1\fnil\fcharset0 LucidaGrande;}
    r'{\colortbl;',
    r'{\*\expandedcolortbl',
    r'{\*\listtable',
    r'{\*\listoverridetable',
    r'\pard',
]


def is_header(line):
    if not line.strip():
        return True
    for prefix in header_markers:
        if line.startswith(prefix):
            return True
    return False


font_pattern = re.compile(r'(?P<fontspec>(\\f(?P<id>\d+)(?P<info>\\.*?) (?P<font_name>.*?));)')


def split_fonts(line):
    fonts = {}
    for match in font_pattern.findall(line):
        fonts[match[2]] = match[4]
    return fonts


def split_rtf(text):
    """Split RTF in header and contents, extract font table."""
    header = []
    contents = []
    in_header = True
    for line in text.strip().split('\n'):
        if not line.strip():
            continue
        if in_header:
            if is_header(line):
                header.append(line)
                continue
            elif line.startswith(r'{\fonttbl'):
                fonts = split_fonts(line)
                header.append(line)
                continue
            else:
                in_header = False
        contents.append(line)

    return dict(header='\n'.join(header), contents='\n'.join(contents)[:-1].strip(), fonts=fonts)
