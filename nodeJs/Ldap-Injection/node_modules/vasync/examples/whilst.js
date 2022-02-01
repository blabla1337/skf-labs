var mod_vasync = require('../lib/vasync');

var n = 0;

var w = mod_vasync.whilst(
    function testFunc() {
        return (n < 5);
    },
    function iterateFunc(cb) {
        n++;
        cb(null, {n: n});
    },
    function whilstDone(err, arg) {
        console.log('err: %j', err);
        console.log('arg: %j', arg);
        console.log('w (end): %j', w);
    }
);

console.log('w (start): %j', w);
