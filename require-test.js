#!/usr/bin/env osascript -l JavaScript
/*
Script to test a simple import function
*/

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

var [partial, print] = require('./modules/test-module.js')

function run (argv) { // eslint-disable-line no-unused-vars
  var finish = partial(console.log, 'finished')

  finish('foo')
  print('x')
}
