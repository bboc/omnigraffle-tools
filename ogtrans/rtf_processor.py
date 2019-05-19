import re
from .rtf2md import rtf2md
from .md2rtf import md2rtf

class RtfObject(object):

    def __init__(self, raw_rtf):
        self.raw_rtf = raw_rtf
        self.fonts = []
        self.header = ''
        self.contents = ''
        self.preprocess()

    def preprocess(self):
        """Extract header, contents and font table."""
        result = split_rtf(self.raw_rtf)
        self.header = result['header']
        self.contents = result['contents']
        self.fonts = result['fonts']

    @property
    def markdown(self):
        return rtf2md(self.contents)

    @markdown.setter
    def markdown(self, value):
        """Create raw_rtf from markdown."""
        self.raw_rtf = '\n'.join(self.header, md2rtf(value))


HEADER_MARKERS = [
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
    for prefix in HEADER_MARKERS:
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
