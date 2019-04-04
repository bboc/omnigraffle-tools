# JXA Resources

- use osacompile to make runnable scripts: https://github.com/dagware/DanThomas/issues/2
- js Module pattern: https://addyosmani.com/resources/essentialjsdesignpatterns/book/#modulepatternjavascript

- Importing Scripts: https://github.com/JXA-Cookbook/JXA-Cookbook/wiki/Importing-Scripts
- Omni Automation: https://omni-automation.com/jxa-applescript.html
- JXA Cookbook: https://github.com/JXA-Cookbook/JXA-Cookbook/wiki
- Beginner's Guide to JXA: https://computers.tutsplus.com/tutorials/a-beginners-guide-to-javascript-application-scripting-jxa--cms-27171
- macOS Automation: http://www.macosxautomation.com
- more JXA Resources: https://apple-dev.groups.io/g/jxa/wiki/JXA-Resources
- https://apple.stackexchange.com/questions/100642/how-to-make-an-existing-applescript-file-to-work-as-a-service
- Mac Scripting: https://developer.apple.com/library/archive/documentation/LanguagesUtilities/Conceptual/MacAutomationScriptingGuide/
- Browserify: https://github.com/browserify/browserify
- KeyboardMaestro and JXA: https://wiki.keyboardmaestro.com/JavaScript_for_Automation
- build CLI tools in nodeJS: https://medium.freecodecamp.org/how-to-build-a-cli-tool-in-nodejs-bc4f67d898ec


## Debugging with Safari

- make sure in the safari develop menu "Automatically Show Web Inspector for JSContexts" is ticket (apparently that becomes unticked time and again)
- open an .scpt file in the script editor (which is a binary format FFS)
- add 'debugger' where you want to open the debugger


## ESLint Setup:

	nmp install -g eslint
	npm install -g eslint-config-standard eslint-plugin-standard eslint-plugin-promise eslint-plugin-import eslint-plugin-node

setup .eslintrc to define standard styleguide: <https://eslint.org/docs/user-guide/configuring>


## Accessing and setting app properties

	OmniGraffle.documents[0].name()
	OmniGraffle.documents[0].canvases[0].name.set("foo")
	OmniGraffle.currentExportSettings.exportScale()
	OmniGraffle.currentExportSettings.areaType()
	OmniGraffle.currentExportSettings.areaType.get()

For some other strange reason (probably due to the way the scripting bridge works), it's not
easy to determine whether or not a property in a scriptable object exists
apparently, sometimes testing for a property makes some nodes disappear?? This happens with id().
	
	# osascript -l JavaScript -i
	>> og = Application('OmniGraffle')
	=> Application("OmniGraffle")
	>> doc = og.open("/Users/beb/dev/ogtool/JXA/test-data/test-data.graffle")
	=> Application("OmniGraffle").documents.byId("kDcL-l0zYTj")
	>> doc.canvases[2].name()
	=> "translatable"
	>> doc.canvases[2].name.get()
	=> "translatable"
	>> doc.foo[5].name()
	!! Error on line 1: Error: Can't convert types.
	>> doc.canvases[5]  // there's only 3 canvases!!
	=> Application("OmniGraffle").documents.byId("kDcL-l0zYTj").canvases.at(5)
	>> doc.canvases[1]
	=> Application("OmniGraffle").documents.byId("kDcL-l0zYTj").canvases.at(1)
	>> doc.canvases[1].name()
	=> "Canvas 2"
	>> doc.canvases[5].name()
	!! Error on line 1: Error: Invalid index.
	>> doc.canvases[2].hasOwnProperty("layers")
	=> true
	>> doc.canvases[2].hasOwnProperty("laXXXyers")
	=> true  // yeah, right ???!!
	
	all objects in OmniGraffle are derived from Item, which has a class propery. We can use that.
	collection groups exists in layers:
	>> doc.canvases[2].layers[0].groups[1].class()
	=> "table"
	>> doc.canvases[2].layers[0].groups[2].class()
	!! Error on line 1: Error: Invalid index.
	
	collection tables does NOT exist in layers
	>> doc.canvases[2].layers[0].tables[0].class()
	!! Error on line 1: Error: Can't convert types.
	
	>> doc.canvases[2].layers[0].groups.length
	=> 2
	>> doc.canvases[2].layers[0].tables.length
	=> Application("OmniGraffle").documents.byId("kDcL-l0zYTj").canvases.at(2).layers.at(0).tables.length
	>> typeof doc.canvases[2].layers[0].tables.length
	=> "function"
	
