
from collections import defaultdict

import polib
import re


BASENAME_PATTERN = re.compile("(?P<basename>[^//]+?)\.graffle(/data\.plist)?$")


def find_basename(path):
    m = BASENAME_PATTERN.search(path)
    return m.group('basename')


class NewTranslationMemory(object):

    def __init__(self):
        self._memory = defaultdict(set)

    def add(self, text, context):
        if text.strip():  # add only text with non-whitespace memory
            # location = "%s/%s" % (file_name, canvas_name)
            self._memory[text.strip()].add(context)

    def dump_translation_memory(self, basename):
        """
        Dump translation memory to a pot-file.

        Sort messages in pot-file by location (if there's more locations, sort locations
        alphabetiaclly first) so that translators can process canvases alphabetially and
        easily review exported images in a folder one by one.
        """
        container = []
        for text, locations in self._memory.items():
            container.append((sorted([l for l in locations]), text))
        container.sort(key=lambda x: x[0][0])

        pot = polib.POFile()
        for locations, text in container:
            entry = polib.POEntry(
                msgid=text,
                msgstr=text,
                occurrences=[(location, '0') for location in locations]
            )
            pot.append(entry)
        pot.save(basename + '.pot')


class TranslationMemoryFile(object):
    """A translation memory that comes from a PO file."""

    def __init__(self, filename):
        self.filename = filename
        self.tm = {}
        self.read_translation_memory()

    def read_translation_memory(self):
        """Read translation memory from a po-file."""
        po = polib.pofile(self.filename)
        for entry in po.translated_entries():
            if not entry.obsolete:
                self.tm[entry.msgid] = entry.msgstr

    def translate(self, text):
        t = text.strip()
        if t and t in self.tm:
            return self.tm[t]
        else:
            raise Exception('text not in translation memory: "%s"' % text)
