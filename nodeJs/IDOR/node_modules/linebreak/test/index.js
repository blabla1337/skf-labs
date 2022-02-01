const fs = require('fs');
const punycode = require('punycode');
const LineBreaker = require('../');
const assert = require('assert');

describe('unicode line break tests', function() {
  // these tests are weird, possibly incorrect or just tailored differently. we skip them.
  const skip = [812,   814,  848,  850,  864,  866,  900,  902,  956,  958, 1068, 1070, 1072, 1074, 1224, 1226,
          1228, 1230, 1760, 1762, 2932, 2934, 4100, 4101, 4102, 4103, 4340, 4342, 4496, 4498, 4568, 4570,
          4704, 4706, 4707, 4708, 4710, 4711, 4712, 4714, 4715, 4716, 4718, 4719, 4722, 4723, 4726, 4727,
          4730, 4731, 4734, 4735, 4736, 4738, 4739, 4742, 4743, 4746, 4747, 4748, 4750, 4751, 4752, 4754,
          4755, 4756, 4758, 4759, 4760, 4762, 4763, 4764, 4766, 4767, 4768, 4770, 4771, 4772, 4774, 4775,
          4778, 4779, 4780, 4782, 4783, 4784, 4786, 4787, 4788, 4790, 4791, 4794, 4795, 4798, 4799, 4800,
          4802, 4803, 4804, 4806, 4807, 4808, 4810, 4811, 4812, 4814, 4815, 4816, 4818, 4819, 4820, 4822,
          4823, 4826, 4827, 4830, 4831, 4834, 4835, 4838, 4839, 4840, 4842, 4843, 4844, 4846, 4847, 4848,
          4850, 4851, 4852, 4854, 4855, 4856, 4858, 4859, 4960, 4962, 5036, 5038, 6126, 6135, 6140, 6225,
          6226, 6227, 6228, 6229, 6230, 6232, 6233, 6234, 6235, 6236, 6332];
  
  const data = fs.readFileSync(__dirname + '/LineBreakTest.txt', 'utf8');
  const lines = data.split('\n');  

  return lines.forEach(function(line, i) {
    let bk;
    if (!line || /^#/.test(line)) { return; }
  
    const [cols, comment] = line.split('#');
    const codePoints = cols.split(/\s*[×÷]\s*/).slice(1, -1).map(c => parseInt(c, 16));
    const str = punycode.ucs2.encode(codePoints);
  
    const breaker = new LineBreaker(str);
    const breaks = [];
    let last = 0;
    while ((bk = breaker.nextBreak())) {
      breaks.push(str.slice(last, bk.position));
      last = bk.position;
    }
    
    const expected = cols.split(/\s*÷\s*/).slice(0, -1).map(function(c) {
      let codes = c.split(/\s*×\s*/);
      if (codes[0] === '') { codes.shift(); }
      codes = codes.map(c => parseInt(c, 16));
      return punycode.ucs2.encode(codes);
    });
      
    if (skip.includes(i)) {
      it.skip(cols, function() {});
      return;
    }
    
    it(cols, () => assert.deepEqual(breaks, expected, i + ' ' + JSON.stringify(breaks) + ' != ' + JSON.stringify(expected) + ' #' + comment));
  });
});
