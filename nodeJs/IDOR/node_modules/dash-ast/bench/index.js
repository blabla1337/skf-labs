var bench = require('nanobench')
var semver = require('semver')
var src = require('fs').readFileSync(require.resolve('acorn'))
var parse = require('acorn').parse
var astw = require('astw')
var eswalk = require('estree-walk')
var dash = require('../')

bench('astw', function (b) {
  var ast = parse(src)
  // warmup
  var i = 0
  for (var x = 0; x < 5; x++) {
    astw(ast)(function (node) { i++ })
  }
  i = 0

  b.start()
  for (x = 0; x < 5; x++) {
    astw(ast)(function (node) { i++ })
  }
  b.end('walked ' + i + ' nodes')
})

bench('estree-walk', function (b) {
  var ast = parse(src)
  // warmup
  var i = 0
  for (var x = 0; x < 5; x++) {
    eswalk(ast, function (node) { i++ })
  }
  i = 0

  b.start()
  for (x = 0; x < 5; x++) {
    eswalk(ast, function (node) { i++ })
  }
  b.end('walked ' + i + ' nodes')
})

bench('estree-walk steps', function (b) {
  var ast = parse(src)
  // warmup
  var i = 0
  for (var x = 0; x < 5; x++) {
    for (var q = [ast], node; (node = q.pop()); eswalk.step(node, q)) {
      i++
    }
  }
  i = 0

  b.start()
  for (x = 0; x < 5; x++) {
    for (q = [ast], node; (node = q.pop()); eswalk.step(node, q)) {
      i++
    }
  }
  b.end('walked ' + i + ' nodes')
})

bench('dash-ast', function (b) {
  var ast = parse(src)
  // warmup
  var i = 0
  for (var x = 0; x < 5; x++) {
    dash(ast, function (node) { i++ })
  }
  i = 0

  b.start()
  for (x = 0; x < 5; x++) {
    dash(ast, function (node) { i++ })
  }
  b.end('walked ' + i + ' nodes')
})

bench('dash-ast with enter/leave', function (b) {
  var ast = parse(src)
  // warmup
  var i = 0
  var j = 0
  for (var x = 0; x < 5; x++) {
    dash(ast, {
      enter: function (node) { i++ },
      leave: function (node) { j++ }
    })
  }
  i = 0
  j = 0

  b.start()
  for (x = 0; x < 5; x++) {
    dash(ast, {
      enter: function (node) { i++ },
      leave: function (node) { j++ }
    })
  }
  b.end('walked ' + [i, j] + ' nodes')
})

if (semver.satisfies(process.version, '>= 8.0.0')) {
  var eswalker = require('estree-walker')

  bench('estree-walker', function (b) {
    var ast = parse(src)
    // warmup
    var i = 0
    for (var x = 0; x < 5; x++) {
      eswalker.walk(ast, {
        enter: function (node) { i++ }
      })
    }
    i = 0

    b.start()
    for (x = 0; x < 5; x++) {
      eswalker.walk(ast, {
        enter: function (node) { i++ }
      })
    }
    b.end('walked ' + i + ' nodes')
  })

  bench('estree-walker with enter/leave', function (b) {
    var ast = parse(src)
    // warmup
    var i = 0
    var j = 0
    for (var x = 0; x < 5; x++) {
      eswalker.walk(ast, {
        enter: function (node) { i++ },
        leave: function (node) { j++ }
      })
    }
    i = 0

    b.start()
    for (x = 0; x < 5; x++) {
      eswalker.walk(ast, {
        enter: function (node) { i++ },
        leave: function (node) { j++ }
      })
    }
    b.end('walked ' + [i, j] + ' nodes')
  })
}
