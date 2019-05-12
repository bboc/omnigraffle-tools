/*

a simple test script to run in Script Editor and use the Safari debugger 

*/

function run(argv) {
	
  var OmniGraffle = Application('OmniGraffle')
  OmniGraffle.includeStandardAdditions = true
  var doc = OmniGraffle.open("/Users/beb/dev/ogtool/JXA/test-data/test-data.graffle")

  debugger;

}