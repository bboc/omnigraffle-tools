
from .rtf_processor import RtfObject


class Translatable(object):
    """Container for a translatable OmniGraffle Object, i.e. an object that contains text."""

    def __init__(self, og_object, context):
        self.og_object = og_object
        self.rtf = RtfObject(self.raw_text)
        self.context = context

    @property
    def raw_text(self):
        return self.og_object['Text']['Text']

    @raw_text.setter
    def raw_text(self, value):
        self.og_object['Text']['Text'] = value

    @property
    def destination(self):
        try:
            return self.og_object['UserInfo']['filename']
        except KeyError:
            return None

    @property
    def maxlength(self):
        try:
            return self.og_object['UserInfo']['maxlength']
        except KeyError:
            return None

    @property
    def klass(self):
        return self.og_object['Class']

