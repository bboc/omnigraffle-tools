function partial (func, ...argsBound) {
  return function (...args) { // (*)
    return func.call(this, ...argsBound, ...args)
  }
}

function print (x) {
  console.log(x)
}

module.exports = [partial, print]
