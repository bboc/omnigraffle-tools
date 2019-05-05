var _ = (function () {
  var action = new PlugIn.Action(function (selection) { // eslint-disable-line no-undef
    // Insert your code here.
    var failedTests = 0

    // add canvasByName to document
    document.constructor.prototype.canvasByName = function (name) {
      return this.portfolio.canvases.find(cnvs => cnvs.name === name)
    }
    // add layerByName to canvas
    var aCanvas = document.portfolio.canvases[0]
    aCanvas.constructor.prototype.layerByName = function (name) { // eslint-disable-line no-undef
      return this.layers.find(lyr => lyr.name === name)
    }

    function assertEqual (a, b, msg) {
      console.log('Test:', msg)
      if (a !== b) {
        console.log('actual:', a)
        console.log('expected:', b)
        console.error('test failed!')
        failedTests += 1
      } else {
        console.info('ok')
      }
    }
    function assertType (object, type, msg) {
      assertEqual(typeof object, type, msg)
    }

    console.log('-------------------- Starting Tests --------------------')

    //canvas.graphicWithName
    // setup
    var notShared = document.canvasByName('Canvas 1').layerByName('not-shared')
    var shared = document.canvasByName('Canvas 1').layerByName('shared')

    console.log('--- make sure prototype functions are working as expected')
    assertEqual(document.canvasByName('Canvas 1').name, 'Canvas 1', 'check canvas 1 name')
    assertEqual(notShared.name, 'not-shared', 'check not-shared layer name')
    assertEqual(shared.name, 'shared', 'check shared layer name')
    console.log('--- making sure layers are set up correctly:')
    assertEqual(notShared.graphics.length, 2, 'check element count in not-shared layer')
    assertEqual(shared.graphics.length, 1, 'check  element count in shared layer')
    assertType(notShared.graphics[0], 'object', 'not-shared.0 should be a shape')
    assertType(notShared.graphics[1], 'object', 'not-shared.1 should be a shape')
    assertType(shared.graphics[0], 'object', 'shared.0 should also be a shape')
    assertEqual(shared.graphics[0].text, 'Text on a shared layer', 'shared.0 should contain correct text ')
    assertType(shared.graphics[1], 'undefined', 'shared.1 should not exist')
    assertType(shared.graphics[0], 'object', 'shared.0 should still be accessible after trying to access invalid element')

    // end of tests
    var alert = new Alert('YAY!', `${failedTests} failed.`) // eslint-disable-line no-undef
    alert.show(function (result) {})
  })
  return action
}())
_ // eslint-disable-line no-unused-expressions
