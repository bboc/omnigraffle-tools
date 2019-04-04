#!/usr/bin/env osascript -l JavaScript
/*
Script to test some stuff
*/

/* ---------- standard require function ------------ */
var require = function (path) {
  if (typeof app === 'undefined') { // eslint-disable-line no-use-before-define
    var app = Application.currentApplication() // eslint-disable-line no-undef
    app.includeStandardAdditions = true
  }
  var handle = app.openForAccess(path)
  var contents = app.read(handle)
  app.closeAccess(path)
  var module = { exports: {} }
  var exports = module.exports // eslint-disable-line no-unused-vars
  eval(contents) // eslint-disable-line no-eval
  return module.exports
}
/* ---------- end standard require function ------------ */

var [writeTextToFile, readFile] = require('./modules/file_io.js')

function run (argv) { // eslint-disable-line no-unused-vars
  var story = 'this is some text'
  // var desktopString = app.pathTo("desktop").toString()
  var file = argv[0]
  writeTextToFile(story, file, true)
}
