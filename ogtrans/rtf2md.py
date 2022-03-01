
import re

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


unicode_characters = re.compile(r'(?P<all>\\uc0\\u(?P<char>-?\d+)(?P<space>\s))')


def unicode_decode(m):

    n = int(m.group('char'))
    if n < 0:
        n = 32767 + abs(n)
    print(chr(n))
    return chr(n) + m.group('space')


REPLACEMENTS = (

    (listmarker_pattern, ''),
    (listelement_pattern, '\n\n- '),
    (bold_pattern, '**\g<styled_text>**'),
    (newline_in_sentences, '\g<char> '),
    (italic_pattern, '_\g<styled_text>_'),
    (linebreaks_pattern, '\n'),
    (double_space_before_word, ' \g<char>'),
    (double_space_after_word, '\g<char> '),
    (content_start, '\g<text>'),
    (unicode_characters, unicode_decode), # must be last so that it does not encode list markers!!
)


def rtf2md(text):
    result = text.strip()
    if result.startswith('\\f'):
        m = content_start.search(result.split('\n')[0])
        result = result[len(m.group('controlwords')):]
    for pattern, repl in REPLACEMENTS:
        result = pattern.sub(repl, result, re.DOTALL)

    # strip all whitespace form each line
    result = '\n'.join([line.strip() for line in result.split('\n')])
    if result.endswith('\\'):
        result = result[:-1]
    return result.strip()
