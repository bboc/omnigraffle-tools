var _ = (function () {
  var action = new PlugIn.Action(function (selection) { // eslint-disable-line no-undef
    // Insert your code here.
    var failedTests = 0
    function assertEqual (a, b, msg) {
      console.log(msg)
      if (a !== b) {
        console.log('actual:', a)
        console.log('expected:', b)
        console.error('test failed!', msg)
        failedTests += 1
      } else {
        console.info('ok')
      }
    }
    function assertType (object, type, msg) {
      assertEqual(typeof object, type, msg)
    }

    console.log('-------------------- Starting Tests --------------------')
    var notShared = canvases[0].layers[0]
    var shared = canvases[0].layers[1]
    assertEqual(notShared.name, 'not-shared', 'check not-shared layer name')
    assertEqual(shared.name, 'shared', 'check shared layer name')
    assertEqual(notShared.graphics.length, 2, 'check element count in not-shared layer')
    assertEqual(shared.graphics.length, 1, 'check  element count in shared layer')
    assertType(notShared.graphics[0], 'object', 'not-shared.0 should be a shape')
    assertType(typeof notShared.graphics[1], 'object', 'not-shared.1 should be a shape')
    assertType(typeof shared.graphics[0], 'object', 'shared.0 should also be a shape')
    assertEqual(shared.graphics[0].text, 'Text on a shared layer', 'shared.0 should contain correct text ')
    assertType(typeof shared.graphics[1], 'undefined', 'shared.1 should not exist')
    assertType(typeof shared.graphics[0], 'object', 'shared.0 should still be accessible after trying to access invalid element')

    // end of tests
    var alert = new Alert('YAY!', `${failedTests} failed.`) // eslint-disable-line no-undef
    alert.show(function (result) {})
  })
  return action
}())
_ // eslint-disable-line no-unused-expressions
