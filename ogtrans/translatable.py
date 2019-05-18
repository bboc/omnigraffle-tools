
from .rtf_processor import RtfObject


class Translatable(object):
    """Container for a translatable OmniGraffle Object, i.e. an object that contains text."""

    def __init__(self, og_object):
        self.og_object = og_object
        self.rtf = RtfObject(self.raw_text)

    @property
    def raw_text(self):
        return self.og_object['Text']['Text']

    @raw_text.setter
    def raw_text(self, value):
        self.og_object['Text']['Text'] = value
