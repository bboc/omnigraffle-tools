#!/usr/bin/env osascript -l JavaScript
/*
A JXA script for translating OmniGraffle documents from the commandline

usage: ./ogtranslate.js <command> <source> <target> <property_1=value_1>...<property_n>=<value_n>

e.g.  # ./ogtranslate.js extract /Users/beb/dev/ogtool/JXA/test-data/test-data.graffle  /Users/beb/tmp/texts.po

# ./ogtranslate.js extract /Users/beb/tmp/pattern-map\ copy.graffle  /Users/beb/tmp/texts.po
for some strange reaseon the full path to the og document and for the target is required

See TODO.taskpaper for notes on accessing objects in OmniGraffle

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

var logger = new SimpleLogger(console.log)

var visitedNodes = new NodesVisited()
var numberOfNodes = 0

const COMMANDS = {
  extract: CommandExtractStrings,
  inject: CommandInjectStrings,
  analyze: CommandAnalyzeObjects
}

const TEXT_CONTAINERS = ['graphic', 'incomingline', 'label', 'line', 'outgoingline', 'shape', 'solid']

function run (argv) { // eslint-disable-line no-unused-vars
  var parameters = setParameters(argv)

  logger.setLogThreshold(logger.DEBUG+5)
  // open app if not already open
  var appOpened = false
  if (!Application('OmniGraffle').running()) { // eslint-disable-line no-undef
    ObjC.import('AppKit') // eslint-disable-line no-undef
    $.NSWorkspace.sharedWorkspace.launchApplication('/Applications/OmniGraffle.app') // eslint-disable-line no-undef
    appOpened = true
  }

  var Command = COMMANDS[parameters.command]
  let cmd = new Command(parameters)

  var OmniGraffle = Application('OmniGraffle') // eslint-disable-line no-undef
  OmniGraffle.includeStandardAdditions = true
  var doc = OmniGraffle.open(parameters.source)

  for (const canvas of doc.canvases()) {
    traverseItems(canvas, cmd.callback)
  }
  doc.close()

  if (appOpened) {
    // close app if it was not already open
    OmniGraffle.close()
  }
  cmd.finish()
  logger.info('...done')
  logger.info(`numberOfNodes ${numberOfNodes}`)
}

function exportName (filename) {
  if (filename.substr(-8, 8) === '.graffle') {
    return filename.substr(0, filename.length - 8)
  } else {
    return filename.concat('.po')
  }
}

function partial (func, ...argsBound) {
  return function (...args) { // (*)
    return func.call(this, ...argsBound, ...args)
  }
}

function CommandExtractStrings (parameters) {
  this.texts = new TextRepository()

  this.extractStrings = function (texts, item, context) {
  // a callback for extracting strings into a TextRepository()

    function itemHasText (item) {
      return (TEXT_CONTAINERS.includes(item.class()))
    }

    if (itemHasText(item) && item.text()) {
      // element has more than zero length accessible text

      logger.debug(`text: "${item.text()}"`)
      texts.addText(item.text(), context)
      // for (const text of item.text.attributeRuns()) {
      //   logger.info('a text', text)
      // }
    }

    // if (has_text && item?.text:
    //  for text in item.text.attribute_runs():
    //    if text.strip():  # add only text with non-whitespace memory
    // TODO: provide canvas, file name and layer name !!
    //      context = "%s/%s" % (?file_name, ?canvas_name ?layer name)
    //      textRepository.[text].add(context)
  }

  this.callback = partial(this.extractStrings, this.texts)
  // need to bind this to texts!!
  this.finish = this.texts.dump.bind(this.texts)
}

function CommandInjectStrings (parameters) {
  this.finish = partial(console.log, 'finished')
  this.callback = function (item, context) {
  }
}

function CommandAnalyzeObjects (parameters) {
  // "analyze" command

  // set up logger to write to file instead of standard output
  function logToFile (file, ...texts) {
    texts.push('\r\n')
    writeTextToFile(texts.join(' '), file)
  }
  logger._logCallback = partial(logToFile, parameters.target)

  this.counter = new ClassCounter()
  this.countClasses = function (counter, item, context) {
    counter.count(item.class())
  }

  this.callback = partial(this.countClasses, this.counter)
  // need to bind this to counter!!
  this.finish = this.counter.dump.bind(this.counter)
}

function traverseItems (item, callback, context = {}, indent = 0) {
  // traverse a document to visit all items
  // logger.info("id:", item.id())
  // if (visitedNodes.contains(item.id())) {
  //   return // don't visit twice!
  // }
  // visitedNodes.append(item.id())
  var children
  numberOfNodes += 1

  logger.logNested(logger.DEBUG, indent, `found a "${item.class()}" {`)
  // FIXME: this breaks it completely, resulting in only 6 Objects (instead of 135 being found)
  // item.id()

  switch (item.class()) {
    case 'canvas':
      // contains graphics, groups, layers, lines, shapes, solids, subgraphs;
      logger.logNested(logger.DEBUG, indent + 1, `name: "${item.name()}"`)
      children = ['layers']
      context.canvas = item.name()
      context.layer = ''
      // children = ['layers', 'graphics', 'groups', 'lines', 'shapes', 'solids', 'subgraphs']
      break
    case 'layer':
    case 'sharedLayer':
      logger.logNested(logger.DEBUG, indent + 1, `name: "${item.name()}"`)
      // logger.logNested(logger.INFO, indent + 1, ` ${item.class()} name: "${item.name()}"`)
      if (!item.visible) {
        return // skip invisible layers
      }
      context.layer = item.name()
      children = ['graphics', 'groups', 'lines', 'solids', 'shapes', 'subgraphs']
      break
    case 'group':
    case 'subgraph': // a group
    case 'table': // a group
      children = ['graphics', 'groups', 'solids', 'shapes', 'subgraphs']
      break
    case 'tableslice':
    case 'row':
    case 'column':
      children = ['graphics']
      break
    case 'graphic':
      // contains incomingLines, lines, outgoingLines, userDataItems;
      children = ['incomingLines', 'lines', 'outgoingLines']
      break
    case 'incomingline':
    case 'outgoingline':
    case 'line':
      children = ['labels']
      break
    case 'shape':
    case 'solid':
    case 'label':
      children = []
      break
    default:
      logger.error(`ERROR unknown class: "${item.class()}"`)
  }

  callback(item, context)

  for (var c of children) {
    // debugger;
    logger.logNested(logger.DEBUG, indent + 1, `checking '${c}' {`)
    try {
      for (var subitem of item[c]()) {
        // FIXME: this next line also makes a difference of 119 / 135 objects found!!
        // let foo = subitem.class()
        traverseItems(subitem, callback, context, indent + 2)
      }
    } catch (error) {
      logger.logNested(logger.DEBUG + 5, indent + 2, `...skipped collection ${c} because of ${JSON.stringify(error)}`)
      // TODO: remove this after everything works
      // throw error
    }
    logger.logNested(logger.DEBUG, indent + 1, '}') // end of collection
  }
  logger.logNested(logger.DEBUG, indent, '}') // end of item
}

function setParameters (argv) {
  // parse commandline parameters, set default properties

  var command = argv[0]
  var source = argv[1]
  var target = argv[2]
  var myproperties = argv.slice(3)
  // TODO: log output can start only AFTER the log target has been determined!!
  logger.debug('Processing OmniGraffle document -------------------------------------------')
  logger.debug(`Command: ${command}`)
  logger.debug(`Source: ${source}`)
  logger.debug(`Target: ${target}`)
  logger.debug(`Properties: ${JSON.stringify(myproperties)}`)

  // set defaults for properties
  var properties = {}

  myproperties.forEach(function (element) {
    var res = element.split('=')
    properties[res[0]] = res[1]
  })

  var parameters = {
    command: command,
    source: source,
    target: target,
    properties: properties
  }

  // TODO: this should be generated from COMMANDS
  var validCommands = ['inject', 'extract', 'analyze']

  if (!validCommands.includes(parameters.command)) {
    throw new Error(`"${parameters.command}" is not a valid command`)
  }
  return parameters
}

function SimpleLogger (callback) {
  this.spacer = '  '
  this._logCallback = callback
  this.DEBUG = 3
  this.INFO = 2
  this.WARNING = 1
  this.ERROR = 0
  this.logThreshold = this.warning

  this.setLogThreshold = function (level) {
    this.logThreshold = level
  }
  this._log = function (level, ...string) {
    if (level <= this.logThreshold) {
      this._logCallback(...string)
    }
  }
  this.logNested = function (level, indent, string) {
    // special logger function to easily visualize a nested object model
    this._log(level, this.spacer.repeat(indent) + string)
  }
  this.error = function (...text) {
    this._log(this.ERROR, ...text)
  }
  this.warning = function (...text) {
    this._log(this.WARNING, ...text)
  }
  this.info = function (...text) {
    this._log(this.INFO, ...text)
  }
  this.debug = function (...text) {
    this._log(this.DEBUG, ...text)
  }
}

function TextRepository () {
  // assoc. array that holds all texts

  this.texts = new Map()
  this.addText = function (text, context) {
    var contents = []
    if (this.texts.has(text)) {
      contents = this.texts.get(text)
    }
    contents.push(context)
    this.texts.set(text, contents)
  }
  this.dump = function () {
    for (var [text, context] of this.texts) {
      logger.info('text', text)
      logger.info('context', JSON.stringify(context))
    }
  }
}

function ClassCounter () {
  this.classes = new Map()
  this.count = function (klass) {
    if (!this.classes.has(klass)) {
      this.classes.set(klass, 1)
    }
    let count = this.classes.get(klass)
    this.classes.set(klass, ++count)
  }
  this.dump = function () {
    for (var [klass, num] of this.classes) {
      logger.info(`${klass} : ${num}`)
    }
  }
}

function NodesVisited () {
  // track ids of visited nodes so that traversing the document is faster
  this.currentFile = ''
  this.currentCanvas = ''
  this.currentLayer = ''
  this._nodes = new Set()

  this.contains = function (id) {
    return this._nodes.has(id)
  }
  this.append = function (id) {
    this._nodes.add(id)
  }
}
