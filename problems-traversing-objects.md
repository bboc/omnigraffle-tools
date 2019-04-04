# Problems traversing objects in the test document

I have a rather curious problem with scripting OmniGraffle through JXA. What I want to do is build a tool for exporting text from OmniGraffle documents into a translation platform, and then taking the translations in inserting them back into those OmniGraffle documents.

However, my code cannot access all items in  OmniGraffle documents.

The issue can be best observed when looking at the code in the branch [feature/fix-traverse-document](https://github.com/bboc/omnigraffle-tools/tree/feature/fix-traverse-document), called like this

> ./ogtranslate.js analyze  /Users/beb/dev/omnigraffle-tools/test-data/test-data.graffle /Users/beb/tmp/analyze.log

(for some reason osascript only handles full paths, so you'd need to adapt that command on your machine)

When the code in [ogexport.js](https://github.com/bboc/omnigraffle-tools/blob/feature/fix-traverse-document/ogtranslate.js) processes the [my test document](https://github.com/bboc/omnigraffle-tools/blob/feature/fix-traverse-document/test-data/test-data.graffle) , and in the attached log file nalyze-case-1-nodes-135.log it's easy to see that errors are thrown in line 163 for some items, when the code tries accessing the class of the first element in certain collections. This happens with all non-empty collections that contain groups, and with all non-empty collections in shared layers. Since according to the documentation in the dictionary all objects in the document tree are derived from Item, all should have a class.

(Note: Line numbers of errors are offset by one line because of the hashbang in the first line which is not present in what the JavaScript interpreter sees.)

This is the same behaviour I observed with my old Python code, but I blamed that on the Python bridge. Now that I ported this to JXA I believe this is a problem with OmniGraffle that is probably really simple to fix. Can you confirm that?

I did what I could to make this problem as transparent as possible, but let me know if you need any more input from my side to understand and resolve this, as this problem prevents me form making progress on a very important project.

