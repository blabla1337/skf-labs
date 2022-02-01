/*
 * Tests the "filter", "filterSeries", and "filterLimit" functions
 */

var mod_util = require('util');

var mod_tap = require('tap');
var mod_vasync = require('..');

mod_tap.test('filterSeries', function (test) {
	var inputs = [0, 1, 2, 3, 4, 5];
	var curTasks = 0;
	var maxTasks = 0;
	// filterSeries has an implicit limit of 1 concurrent operation
	var limit = 1;

	function filterFunc(input, cb) {
		curTasks++;
		if (curTasks > maxTasks) {
			maxTasks = curTasks;
		}
		test.ok(curTasks <= limit, mod_util.format(
		    'input %d: current tasks %d <= %d',
		    input, curTasks, limit));

		setTimeout(function () {
			curTasks--;
			cb(null, input < 2 || input === 4);
		}, 50);
	}

	mod_vasync.filterSeries(inputs, filterFunc,
	    function filterDone(err, results) {

		test.ok(!err, 'error unset');
		test.equal(maxTasks, limit, 'max tasks reached limit');
		test.deepEqual(results, [0, 1, 4], 'results array correct');
		test.end();
	});
});

mod_tap.test('filterLimit', function (test) {
	var inputs = [0, 1, 2, 3, 4, 5];
	var curTasks = 0;
	var maxTasks = 0;
	var limit = 2;

	function filterFunc(input, cb) {
		curTasks++;
		if (curTasks > maxTasks) {
			maxTasks = curTasks;
		}
		test.ok(curTasks <= limit, mod_util.format(
		    'input %d: current tasks %d <= %d',
		    input, curTasks, limit));

		setTimeout(function () {
			curTasks--;
			cb(null, input < 2 || input === 4);
		}, 50);
	}

	mod_vasync.filterLimit(inputs, limit, filterFunc,
	    function filterDone(err, results) {

		test.ok(!err, 'error unset');
		test.equal(maxTasks, limit, 'max tasks reached limit');
		test.deepEqual(results, [0, 1, 4], 'results array correct');
		test.end();
	});
});

mod_tap.test('filter (maintain order)', function (test) {
	var inputs = [0, 1, 2, 3, 4, 5];
	var limit = inputs.length;
	var storedValues = [];

	function filterFunc(input, cb) {
		/*
		 * Hold every callback in an array to be called when all
		 * filterFunc's have run.  This way, we can ensure that all
		 * tasks have started without waiting for any others to finish.
		 */
		storedValues.push({
			input: input,
			cb: cb
		});

		test.ok(storedValues.length <= limit, mod_util.format(
		    'input %d: current tasks %d <= %d',
		    input, storedValues.length, limit));

		/*
		 * When this constraint is true, all filterFunc's have run for
		 * each input.  We now call all callbacks in a pre-determined
		 * order (out of order of the original) to ensure the final
		 * array is in the correct order.
		 */
		if (storedValues.length === inputs.length) {
			[5, 2, 0, 1, 4, 3].forEach(function (i) {
				var o = storedValues[i];
				o.cb(null, o.input < 2 || o.input === 4);
			});
		}
	}

	mod_vasync.filter(inputs, filterFunc,
	    function filterDone(err, results) {

		test.ok(!err, 'error unset');
		test.equal(storedValues.length, inputs.length,
		    'max tasks reached limit');
		test.deepEqual(results, [0, 1, 4], 'results array correct');
		test.end();
	});
});

mod_tap.test('filterSeries error handling', function (test) {
	/*
	 * We will error half way through the list of inputs to ensure that
	 * first half are processed while the second half are ignored.
	 */
	var inputs = [0, 1, 2, 3, 4, 5];

	function filterFunc(input, cb) {
		switch (input) {
		case 0:
		case 1:
		case 2:
			cb(null, true);
			break;
		case 3:
			cb(new Error('error on ' + input));
			break;
		case 4:
		case 5:
			test.ok(false, 'processed too many inputs');
			cb(new Error('processed too many inputs'));
			break;
		default:
			test.ok(false, 'unexpected input: ' + input);
			cb(new Error('unexpected input'));
			break;
		}
	}

	mod_vasync.filterSeries(inputs, filterFunc,
	    function filterDone(err, results) {

		test.ok(err, 'error set');
		test.ok(err.message === 'error on 3', 'error on input 3');
		test.ok(results === undefined, 'results is unset');
		test.end();
	});
});

mod_tap.test('filterSeries double callback', function (test) {
	var inputs = [0, 1, 2, 3, 4, 5];

	function filterFunc(input, cb) {
		switch (input) {
		case 0:
		case 1:
		case 2:
			cb(null, true);
			break;
		case 3:
			/*
			 * The first call to cb() should "win" - meaning this
			 * value will be filtered out of the final array of
			 * results.
			 */
			cb(null, false);
			test.throws(function () {
				cb(null, true);
			});
			break;
		case 4:
			/*
			 * Like input 3, all subsequent calls to cb() will
			 * throw an error and not affect the original call to
			 * cb().
			 */
			cb(null, true);
			test.throws(function () {
				cb(new Error('uh oh'));
			});
			break;
		case 5:
			cb(null, true);
			break;
		default:
			test.ok(false, 'unexpected input: ' + input);
			cb(new Error('unexpected input'));
			break;
		}
	}

	mod_vasync.filterSeries(inputs, filterFunc,
	    function filterDone(err, results) {

		test.ok(!err, 'error not set');
		test.deepEqual(results, [0, 1, 2, 4, 5],
		    'results array correct');
		test.end();
	});
});

mod_tap.test('filter push to queue object error', function (test) {
	var inputs = [0, 1, 2, 3, 4, 5];

	function filterFunc(input, cb) {
		cb(null, true);
	}

	var q = mod_vasync.filterSeries(inputs, filterFunc,
	    function filterDone(err, results) {

		test.end();
	});

	test.equal(q.closed, true, 'queue is closed');
	test.throws(function () {
		q.push(6);
	});
});
