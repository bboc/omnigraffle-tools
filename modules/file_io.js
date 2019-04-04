/* code from https://developer.apple.com/library/archive/documentation/LanguagesUtilities/Conceptual/MacAutomationScriptingGuide/ReadandWriteFiles.html */

var app = Application.currentApplication() // eslint-disable-line no-undef
app.includeStandardAdditions = true

function writeTextToFile (text, file, overwriteExistingContent=false) {
  try {
    // Convert the file to a string
    var fileString = file.toString()

    // Open the file for writing
    var openedFile = app.openForAccess(Path(fileString), { writePermission: true }) // eslint-disable-line no-undef

    // Clear the file if content should be overwritten
    if (overwriteExistingContent) {
      app.setEof(openedFile, { to: 0 })
    }

    // Write the new content to the file
    app.write(text, { to: openedFile, startingAt: app.getEof(openedFile) })

    // Close the file
    app.closeAccess(openedFile)

    // Return a boolean indicating that writing was successful
    return true
  } catch (error) {
    try {
      // Close the file
      app.closeAccess(file)
    } catch (error) {
      // Report the error is closing failed
      console.log(`Couldn't close file: ${error}`)
    }
    // Return a boolean indicating that writing was successful
    return false
  }
}

function readFile (file) {
  // Convert the file to a string
  var fileString = file.toString()

  // Read the file and return its contents
  return app.read(Path(fileString)) // eslint-disable-line no-undef
}

function readAndSplitFile (file, delimiter) { // eslint-disable-line no-unused-vars
  // Convert the file to a string
  var fileString = file.toString()

  // Read the file using a specific delimiter and return the results
  return app.read(Path(fileString), { usingDelimiter: delimiter }) // eslint-disable-line no-undef
}

module.exports = [writeTextToFile, readFile]
