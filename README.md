# omnigraffle-tools

A set of commandline tools for [OmniGraffle 6+](http://www.omnigroup.com/products/omnigraffle/), for export, translation, replacement of fonts and colors etc. Comes with a plugin API to that allows for simple manipulation of items in OmniGraffle documents.

For now this is an experiment, I am trying to port the major features of my Python project [ogtool](https://github.com/bboc/ogtool) to JavaScript for Applications (JXA), to find out whether or not JXA is a way forward for _ogtool_.

One part of this experiment is working with OmniGraffle support to figure out which of the known issues encountered in _ogtool_ were in fact related to _py-appscript_, and which might be issues in OmniGraffle that can be resolved on their side.

TODOs, including other small issues and more notes are tracked in [TODO.taskpaper](TODO.taskpaper), resources about. JXA are collected in [JXA-Resources.md](JXA-Resources.md).

## Known Issues of ogtool (Python)

1. **og-tools cannot access objects shared layers properly**. It appeared that this might be caused by py-appscript. Since py-appscript is unmaintained for quite a few years now, this issue will most likely not be fixed anytime soon. An effective workaround might be toggling the shared layers before and after processing, either manually, or maybe through AppleScript/JavsScript or even with py-appscript. **It appears now that this issue is still present when accessing OmniGraffle through JXA**
2. **ogtranslate currently does not translate line labels.** fi
3. **obtools test suite is incomplete** The test suite only covers omnigraffle_export and ogexport, and needs to be extended for ogtool and ogtranslate. _I need to figure an elegant way to write tests for my JXA code._
4. **replacing text in attribute runs does not result in the document being marked as updated**, so injected tranlsations are not saved. The code contains a workaround - adding a timestamp to key 'upd_timestamp' in user data of the element containing the text - so that the element with replaced text is marked as updated. This problem is at least present in OmniGraffle 6.6.2 and can be observed through watching document.modified(). This does not only affect attribute runs, I also observed this when changing colors, user_names and font size. According to the OmniGraffle developers this behaviour has not changed in version 7. 


## Changelog

...
