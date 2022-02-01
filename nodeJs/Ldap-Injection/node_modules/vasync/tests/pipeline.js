/*
 * Tests the "pipeline" primitive.
 */

var mod_tap = require('tap');
var mod_vasync = require('..');
var st;


mod_tap.test('empty pipeline', function (test) {
	var count = 0;
	st = mod_vasync.pipeline({'funcs': [], 'arg': null},
	    function (err, result) {

		test.ok(err === null);
		test.ok(result.ndone === 0);
		test.ok(result.nerrors === 0);
		test.ok(result.operations.length === 0);
		test.ok(result.successes.length === 0);
		test.equal(count, 1);
		test.end();
	});
	count++;
	test.ok(st.ndone === 0);
	test.ok(st.nerrors === 0);
	test.ok(st.operations.length === 0);
	test.ok(st.successes.length === 0);
});

mod_tap.test('normal 4-stage pipeline', function (test) {
	var count = 0;
	st = mod_vasync.pipeline({'funcs': [
		function func1(_, cb) {
			test.equal(st.successes[0], undefined,
				'func1: successes');
			test.ok(count === 0, 'func1: count === 0');
			test.ok(st.ndone === 0);
			count++;
			setImmediate(cb, null, count);
		},
		function func2(_, cb) {
			test.equal(st.successes[0], 1, 'func2: successes');
			test.ok(count == 1, 'func2: count == 1');
			test.ok(st.ndone === 1);
			test.ok(st.operations[0].status == 'ok');
			test.ok(st.operations[1].status == 'pending');
			test.ok(st.operations[2].status == 'waiting');
			count++;
			setImmediate(cb, null, count);
		},
		function (_, cb) {
			test.equal(st.successes[0], 1, 'func3: successes');
			test.equal(st.successes[1], 2, 'func3: successes');
			test.ok(count == 2, 'func3: count == 2');
			test.ok(st.ndone === 2);
			count++;
			setImmediate(cb, null, count);
		},
		function func4(_, cb) {
			test.equal(st.successes[0], 1, 'func4: successes');
			test.equal(st.successes[1], 2, 'func4: successes');
			test.equal(st.successes[2], 3, 'func4: successes');
			test.ok(count == 3, 'func4: count == 3');
			test.ok(st.ndone === 3);
			count++;
			setImmediate(cb, null, count);
		}
	]}, function (err, result) {
		test.ok(count == 4, 'final: count == 4');
		test.ok(err === null, 'no error');
		test.ok(result === st);
		test.equal(result, st, 'final-cb: st == result');
		test.equal(st.successes[0], 1, 'final-cb: successes');
		test.equal(st.successes[1], 2, 'final-cb: successes');
		test.equal(st.successes[2], 3, 'final-cb: successes');
		test.equal(st.successes[3], 4, 'final-cb: successes');
		test.ok(st.ndone === 4);
		test.ok(st.nerrors === 0);
		test.ok(st.operations.length === 4);
		test.ok(st.successes.length === 4);
		test.ok(st.operations[0].status == 'ok');
		test.ok(st.operations[1].status == 'ok');
		test.ok(st.operations[2].status == 'ok');
		test.ok(st.operations[3].status == 'ok');
		test.end();
	});
	test.ok(st.ndone === 0);
	test.ok(st.nerrors === 0);
	test.ok(st.operations.length === 4);
	test.ok(st.operations[0].funcname == 'func1', 'func1 name');
	test.ok(st.operations[0].status == 'pending');
	test.ok(st.operations[1].funcname == 'func2', 'func2 name');
	test.ok(st.operations[1].status == 'waiting');
	test.ok(st.operations[2].funcname == '(anon)', 'anon name');
	test.ok(st.operations[2].status == 'waiting');
	test.ok(st.operations[3].funcname == 'func4', 'func4 name');
	test.ok(st.operations[3].status == 'waiting');
	test.ok(st.successes.length === 0);
});

mod_tap.test('bailing out early', function (test) {
	var count = 0;
	st = mod_vasync.pipeline({'funcs': [
		function func1(_, cb) {
			test.ok(count === 0, 'func1: count === 0');
			count++;
			setImmediate(cb, null, count);
		},
		function func2(_, cb) {
			test.ok(count == 1, 'func2: count == 1');
			count++;
			setImmediate(cb, new Error('boom!'));
		},
		function func3(_, cb) {
			test.ok(count == 2, 'func3: count == 2');
			count++;
			setImmediate(cb, null, count);
		}
	]}, function (err, result) {
		test.ok(count == 2, 'final: count == 3');
		test.equal(err.message, 'boom!');
		test.ok(result === st);
		test.equal(result, st, 'final-cb: st == result');
		test.ok(st.ndone == 2);
		test.ok(st.nerrors == 1);
		test.ok(st.operations[0].status == 'ok');
		test.ok(st.operations[1].status == 'fail');
		test.ok(st.operations[2].status == 'waiting');
		test.ok(st.successes.length == 1);
		test.end();
	});
});
