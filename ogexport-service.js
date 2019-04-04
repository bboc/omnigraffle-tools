var app = Application.currentApplication()
app.includeStandardAdditions = true

function run(input, parameters) {


    // open Omnigraffle
    OmniGraffle = Application('OmniGraffle')
    OmniGraffle.includeStandardAdditions = true

    // export each document
    const result = input.map(exportDocument);


    // prepare output
    const dialogText = "Exported documents \n\n" + (result.reduce(combineOutput, ""))
    // display confirmation
    app.displayDialog(dialogText)
    return result
}

function combineOutput(result, tuple) {

    return result.concat(tuple[0], "\n")
}

function exportDocument(file) {
    var doc = OmniGraffle.open(file)
    var target = exportName(file+"")
    doc.export({as:"PNG", 
                scope:"entire document", 
                to:Path(target), 
                withProperties: {scale:1,
                                 resolution:1.94444441795
                                }
              })
    doc.close()
    return [file, target]
}

function exportName(filename) {
  if (filename.substr(-8, 8) === ".graffle") { 
    return filename.substr(0,filename.length - 8)
  } else {
    return filename.concat(".out")
  }
}
