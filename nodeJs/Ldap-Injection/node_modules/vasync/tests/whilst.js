/*
 * Tests the "whilst" function
 */

var mod_util = require('util');

var mod_tap = require('tap');
var mod_vasync = require('..');

mod_tap.test('basic whilst', function (test) {
	var n = 0;

	mod_vasync.whilst(
	    function condition() {
		return (n < 5);
	    },
	    function body(cb) {
		n++;
		cb(null, n);
	    },
	    function done(err, arg) {
		test.ok(!err, 'error unset');
		test.equal(n, 5, 'n == 5');
		test.equal(n, arg, 'n == arg');
		test.end();
	    });
});

mod_tap.test('whilst return object', function (test) {
	var n = 0;

	var w = mod_vasync.whilst(
	    function condition() {
		return (n < 5);
	    },
	    function body(cb) {
		n++;

		test.equal(n, w.iterations, 'n == w.iterations: ' + n);

		cb(null, n, 'foo');
	    },
	    function done(err, arg1, arg2, arg3) {
		test.ok(!err, 'error unset');
		test.equal(w.iterations, 5, 'whilst had 5 iterations');
		test.equal(w.finished, true, 'whilst has finished');
		test.equal(arg1, n, 'whilst arg1 == n');
		test.equal(arg2, 'foo', 'whilst arg2 == "foo"');
		test.equal(arg3, undefined, 'whilst arg3 == undefined');
		test.end();
	    });

	test.equal(typeof (w), 'object', 'whilst returns an object');
	test.equal(w.finished, false, 'whilst is not finished');
	test.equal(w.iterations, 0, 'whilst has not started yet');
});

mod_tap.test('whilst false condition', function (test) {
	mod_vasync.whilst(
	    function condition() {
		return (false);
	    },
	    function body(cb) {
		cb();
	    },
	    function done(err, arg) {
		test.ok(!err, 'error is unset');
		test.ok(!arg, 'arg is unset');
		test.end();
	    });
});

mod_tap.test('whilst error', function (test) {
	var n = 0;

	var w = mod_vasync.whilst(
	    function condition() {
		return (true);
	    },
	    function body(cb) {
		n++;

		if (n > 5) {
			cb(new Error('n > 5'), 'bar');
		} else {
			cb(null, 'foo');
		}
	    },
	    function done(err, arg) {
		test.ok(err, 'error is set');
		test.equal(err.message, 'n > 5');
		test.equal(arg, 'bar');

		test.equal(w.finished, true, 'whilst is finished');

		/*
		 * Iterations is bumped after the test condition is run and
		 * before the iteration function is run.  Because the condition
		 * in this example is inside the iteration function (the test
		 * condition always returns true), the iteration count will be
		 * 1 higher than expected, since it will fail when (n > 5), or
		 * when iterations is 6.
		 */
		test.equal(w.iterations, 6, 'whilst had 6 iterations');

		test.end();
	    });
});
