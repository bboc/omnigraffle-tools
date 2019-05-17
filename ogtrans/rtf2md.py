
import re

from textwrap import dedent

"""
TODO: check other bullet types
TODO: nested lists??
TODO: special characters (like  ➤ 
TODO: encode/decode unicode characters
TODO: bold/regular/italics using OpenSans
"""

bold_pattern = re.compile(r'\\b\s+(?P<styled_text>.+?)\s+\\b0', re.DOTALL)
italic_pattern = re.compile(r'\\i\s+(?P<styled_text>.+?)\s+\\i0', re.DOTALL)

linebreaks_pattern = re.compile(r'(\\)\n', re.DOTALL)

listelement_pattern = re.compile(r'(?P<list_element_prefix>\{\\listtext\s\\f\d\s(?P<bullet>\\uc0\\u9642)\s\\f\d\s+\})', re.DOTALL)
listmarker_pattern = re.compile(r'\\ls\d\\ilvl\d\s', re.DOTALL)

# TODO: \\\n marks a line break in rtf all others can go
newline_in_sentences = re.compile(r'(?P<char>\w)\n')
# TODO: all double whitespace afte the first word character should go
double_space_before_word = re.compile(r'\s\s(?P<char>\w)')
double_space_after_word = re.compile(r'(?P<char>\w)\s\s')

# split text and control words on beginning of line that are not unicode strings
content_start = re.compile(r'^(?P<controlwords>((\\[^\su]\S*)\s)+)(?P<text>.*)')

replacements = (

    (listmarker_pattern, ''),
    (listelement_pattern, '\n\n- '),
    (bold_pattern, '**\g<styled_text>**'),
    (newline_in_sentences, '\g<char> '),
    (italic_pattern, '_\g<styled_text>_'),
    (linebreaks_pattern, '\n'),
    (double_space_before_word, ' \g<char>'),
    (double_space_after_word, '\g<char> '),
    (content_start, '\g<text>'),
)


def rtf2md(text):
    result = text.strip()
    if result.startswith('\\f'):
        m = content_start.search(result.split('\n')[0])
        result = result[len(m.group('controlwords')):]
    for pattern, repl in replacements:
        result = pattern.sub(repl, result, re.DOTALL)

    # strip all whitespace form each line
    result = '\n'.join([line.strip() for line in result.split('\n')])
    if result.endswith('\\'):
        result = result[:-1]
    return result.strip()


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
