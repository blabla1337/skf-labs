'use strict';

var validation = require('../lib/index')
, app = require('./app')
, should = require('should')
, request = require('supertest');

describe('validate query', function () {

  describe('when the request contains a valid query', function () {
    
    it('should return a 200 ok response', function (done) {
      request(app)
        .get('/search?q=true')
        .expect(200)
        .end(function (err, res) {
          var response = JSON.parse(res.text);
          response.should.equal(200);
          done();
        });
    });
  });

  describe('when the request contains an invalid query', function () {
    
    it('should return a 400 response', function (done) {
      request(app)
        .get('/search?q=')
        .expect(400)
        .end(function (err, res) {
          var response = JSON.parse(res.text);
          response.errors.length.should.equal(1);
          done();
        });
    });
  });
});