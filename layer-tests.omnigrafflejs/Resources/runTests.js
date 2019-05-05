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
    // various assertions
    function fail (msg) {
      console.error('Test failed:', msg)
      failedTests += 1
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
    function assertType (obj, type, msg) {
      assertEqual(typeof obj, type, msg)
    }
    function assertClass (obj, cls, msg) {
      try {
        assertEqual(obj.constructor.name, cls, msg)
      } catch (error) {
        fail(msg + ' !!object does not exist!!')
      }
    }

    console.log('-------------------- Starting Tests --------------------')

    // quickly run tests while developing:
    //  - deploy plugin to OmniGraffle via build cmd (makefile with open command)
    //  - use keyboard to replace "replace plugin" (full keyboard access in keyboard preference pane helps)
    //  - running the plugin (via keyboard shortcut set up in BTT) !! wait a second, OmniGraffle is quite slow to update the plugin, if you're too fast, old code is run

    // setup
    var cnvs1 = document.canvasByName('Canvas 1')
    var notShared = cnvs1.layerByName('not-shared')
    var shared = cnvs1.layerByName('shared')
    console.clear()

    function testBasics () {
      console.log('--- make sure prototype functions are working as expected')
      assertEqual(cnvs1.name, 'Canvas 1', 'check canvas 1 name')
      assertEqual(notShared.name, 'not-shared', 'check not-shared layer name')
      assertEqual(shared.name, 'shared', 'check shared layer name')

      console.log('--- making sure layers are set up correctly:')
      assertEqual(notShared.graphics.length, 2, 'check element count in not-shared layer')
      assertEqual(shared.graphics.length, 1, 'check  element count in shared layer')
    }

    function testGraphicsWithName () {
      console.log('--- test accessing graphics via index and via canvas.graphicsWithName()')
      assertClass(notShared.graphics[0], 'Shape', 'not-shared.0 should be a shape')
      assertClass(notShared.graphics[1], 'Shape', 'not-shared.1 should be a shape')

      var ncName = 'normal-circle'
      assertClass(cnvs1.graphicWithName(ncName), 'Shape', 'access of normal-circle via graphicsWithName()')
      assertEqual(cnvs1.graphicWithName(ncName).name, ncName, 'access name of normal-circle via graphicsWithName()')
      assertEqual(cnvs1.graphicWithName(ncName).text, 'Text in normal-circle', 'access text of normal-circle via graphicsWithName()')
    }

    function testSharedLayerAccess () {
      console.log('--- access text on shared layer:')
      var scName = 'shared-circle'
      assertClass(shared.graphics[0], 'Shape', 'shared.0 should also be a shape')
      assertEqual(shared.graphics[0].name, scName, 'access of shared.0.name via index')
      assertEqual(shared.graphics[0].text, 'Text on a shared layer', 'access shared.0.text via index')

      assertClass(cnvs1.graphicWithName(scName), 'Shape', 'access of shared-circle via graphicsWithName()')
      assertEqual(cnvs1.graphicWithName(scName).name, scName, 'access name of shared-circle via graphicsWithName()')
      assertEqual(cnvs1.graphicWithName(scName).text, 'Text on a shared layer', 'access text of shared-circle via graphicsWithName()')
    }

    function testElementAccessBug () {
      console.log('--- known bug: accessing an element in a shared layer after attempting to access an element that does not exist in that layer:')
      assertEqual(shared.graphics[0].text, 'Text on a shared layer', 'retrieve text from shared.0')
      var idx = shared.graphics.length + 1
      assertType(shared.graphics[idx], 'undefined', 'this element should not exist')
      assertEqual(shared.graphics[idx].text, '', 'undefined object should return no text')
      assertEqual(shared.graphics[0].text, 'Text on a shared layer', 'text in shared.0 is still accessible')
    }

    function testSubgraphTextBug () {
      console.log('--- known Bug: subgraphs return no text data')
      fail('test not implemented')
    }

    function testGroupTextBug () {
      console.log('--- known Bug: groups return no text data')
      fail('test not implemented')
    }

    function testTableTextBug () {
      console.log('--- known Bug: tables return no text data')
      fail('test not implemented')
    }
    /// run the test suite

    //testBasics()
    //testGraphicsWithName()
    testSharedLayerAccess()
    // testElementAccessBug()
    // testSubgraphTextBug()
    // testGroupTextBug()
    // testTableTextBug()

    // end of tests
    console.info(`--- test finished, ${failedTests} tests failed.`)
    var alert = new Alert('YAY!', `${failedTests} failed.`) // eslint-disable-line no-undef
    alert.show(function (result) {})
  })
  return action
}())
_ // eslint-disable-line no-unused-expressions
