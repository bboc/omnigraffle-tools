var _ = (function () {
  var action = new PlugIn.Action(function (selection) { // eslint-disable-line no-undef
    // Insert your code here.
    console.log('Calling the debugger now')
    debugger
    console.log('after teh debugger!')
    var alert = new Alert('YAY!', 'Dude, that\'s pretty sweet.') // eslint-disable-line no-undef
    alert.show(function (result) {})
  })
  return action
}())
_ // eslint-disable-line no-unused-expressions
