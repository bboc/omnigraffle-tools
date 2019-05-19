
from textwrap import dedent
import plistlib

from .path import Path
from .translatable import Translatable


class PlistWalker(object):

    INDENTATION = '    '

    def __init__(self, filename, verbose=False):
        self.verbose = verbose
        self.path = Path()
        fp = open(filename, 'rb')
        self.doc = plistlib.load(fp, fmt=plistlib.FMT_XML)

    def walk_plist(self, current, level=0, name=''):
        def tabbed(*args):
            if self.verbose:
                indent = level * self.INDENTATION
                print(indent[:-1], *args) # noqa

        def node_value(item):
            if type(item) == bytes:
                return '<bytes>'
            elif type(item) == str:
                if item.startswith(r'{\rtf'):
                    return 'RTF-TEXT'
            return item

        # tabbed(self.path.to_string())

        # do whatever with this item...
        self.selector(current)

        if type(current) == list:
            tabbed('%s [' % name)
            for idx, item in enumerate(current):
                self.path.append_list_item(idx, item)
                self.walk_plist(item, level + 1)
                self.path.pop()
            tabbed(']')
        elif type(current) == dict:
            if name:
                tabbed('%s {' % name)
            else:
                tabbed('{')
            for key, item in current.items():
                self.path.append('.%s' % key)
                self.walk_plist(item, level + 1, key)
                self.path.pop()
            tabbed('}')
        else:
            value = node_value(current)
            tabbed(name, ':', node_value(current))
            if value == 'RTF-TEXT':
                tabbed(self.path.to_string())

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
        self.translatables = []
        super().__init__(filename)

    def selector(self, current):
        if self.is_text_container(current) and self.has_text(current):
            self.translatables.append(Translatable(current, self.path.to_string()))

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

    def collect_translatables(self, canvas=None):
        for canvas in self.doc['Sheets']:
            # TODO: add filter for single canvas here
            self.path = Path(canvas['SheetTitle'])
            self.walk_plist(canvas)
