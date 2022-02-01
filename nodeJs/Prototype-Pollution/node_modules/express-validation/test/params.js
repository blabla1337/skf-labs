'use strict';

var validation = require('../lib/index')
, app = require('./app')
, should = require('should')
, request = require('supertest');

describe('validate params', function () {

  describe('when the request contains a valid parameter', function () {
    
    it('should return a 200 ok response', function (done) {
      request(app)
        .get('/account/1')
        .expect(200)
        .end(function (err, res) {
          res.body.id.should.equal(1);
          done();
        });
    });
  });

  describe('when the request contains an invalid parameter', function () {
    
    it('should return a 400 response', function (done) {
      request(app)
        .get('/account/a')
        .expect(400)
        .end(function (err, res) {
          res.body.errors.length.should.equal(1);
          done();
        });
    });
  });
});