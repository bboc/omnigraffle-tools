

class Path(object):
    def __init__(self, root=''):
        if root:
            self._path = [root]
        else:
            self._path = []

    def to_string(self):
        return ''.join(self._path)

    def append(self, text):
        self._path.append(text)

    def append_list_item(self, index, subitem):
        if isinstance(subitem, dict) and 'Name' in subitem:
            print(subitem['Name'])
            self.append('[%s:%s]' % (index, subitem['Name']))
        else:
            self.append('[%s]' % index)

    def pop(self):
        self._path.pop()
