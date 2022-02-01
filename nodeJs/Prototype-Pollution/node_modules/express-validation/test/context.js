'use strict';
require('should');
var app = require('./app');
var request = require('supertest');

describe('for validating array values', function () {
  describe('when the schema contains a reference to the request object', function () {
    it('should return a 200 ok response', function (done) {
      request(app)
        .post('/context/1')
        .send({ id: '1' })
        .expect(200)
        .end(function (err, res) {
          if (err) {
            return done(err);
          }
          done();
        });
    });
  });

  describe('when the schema contains an invalid reference to the request object', function () {
    it('should return a 400 response', function (done) {
      request(app)
        .post('/context/1')
        .send({ id: '2' })
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
