require('should');
var app = require('./app');
var request = require('supertest');

describe('for validating  array values', function () {
  describe('when the schema contains an array reference', function () {
    it('should return a 200 ok response', function (done) {
      request(app)
        .post('/array')
        .send({ numbers: [1, 2, 3], validate_numbers: [1, 2] })
        .expect(200)
        .end(function (err, res) {
          if (err) {
            return done(err);
          }
          done();
        });
    });
  });

  describe('when the schema contains an invalid array reference', function () {
    it('should return a 400 response', function (done) {
      request(app)
        .post('/array')
        .send({ numbers: [1, 2, 3], validate_numbers: [4, 5] })
        .expect(400)
        .end(function (err, res) {
          if (err) {
            return done(err);
          }
          done();
        });
    }); 
  });
});
