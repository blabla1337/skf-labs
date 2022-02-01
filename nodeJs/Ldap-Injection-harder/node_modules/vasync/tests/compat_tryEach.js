var async = require('../lib/vasync');

/*
 * tryEach tests, transliterated from mocha to tap.
 *
 * They are nearly identical except for some details related to vasync. For
 * example, we don't support calling the callback more than once from any of
 * the given functions.
 */


exports['tryEach no callback'] = function (test) {
    async.tryEach([]);
    test.done();
};
exports['tryEach empty'] = function (test) {
    async.tryEach([], function (err, results) {
        test.equals(err, null);
        test.same(results, undefined);
        test.done();
    });
};
exports['tryEach one task, multiple results'] = function (test) {
    var RESULTS = ['something', 'something2'];
    async.tryEach([
        function (callback) {
            callback(null, RESULTS[0], RESULTS[1]);
        }
    ], function (err, results) {
        test.equals(err, null);
        test.same(results, RESULTS);
        test.done();
    });
};
exports['tryEach one task'] = function (test) {
    var RESULT = 'something';
    async.tryEach([
        function (callback) {
            callback(null, RESULT);
        }
    ], function (err, results) {
        test.equals(err, null);
        test.same(results, RESULT);
        test.done();
    });
};
exports['tryEach two tasks, one failing'] = function (test) {
    var RESULT = 'something';
    async.tryEach([
        function (callback) {
            callback(new Error('Failure'), {});
        },
        function (callback) {
            callback(null, RESULT);
        }
    ], function (err, results) {
        test.equals(err, null);
        test.same(results, RESULT);
        test.done();
    });
};
exports['tryEach two tasks, both failing'] = function (test) {
    var ERROR_RESULT = new Error('Failure2');
    async.tryEach([
        function (callback) {
            callback(new Error('Should not stop here'));
        },
        function (callback) {
            callback(ERROR_RESULT);
        }
    ], function (err, results) {
        test.equals(err, ERROR_RESULT);
        test.same(results, undefined);
        test.done();
    });
};
exports['tryEach two tasks, non failing'] = function (test) {
    var RESULT = 'something';
    async.tryEach([
        function (callback) {
            callback(null, RESULT);
        },
        function () {
            test.fail('Should not been called');
        }
    ], function (err, results) {
        test.equals(err, null);
        test.same(results, RESULT);
        test.done();
    });
};
