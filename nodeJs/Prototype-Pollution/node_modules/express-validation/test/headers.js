'use strict';

var validation = require('../lib/index')
, app = require('./app')
, should = require('should')
, request = require('supertest');

describe('validate headers', function () {

  describe('when the request contains a valid header', function () {
    it('should return a 200 ok response', function (done) {

      request(app)
        .get('/user')
        .set('accessToken', '4343434343')
        .set('userId', '3243243242')
        .expect(200)
        .end(function (err, res) {
          var response = JSON.parse(res.text);
          response.should.equal(200);
          done();
        });
    });
  });

  describe('when the request contains an invalid header', function () {
    it('should return a 200 ok response', function (done) {

      request(app)
        .get('/user')
        .set('accessToken', '')
        .set('userId', '3243243242')
        .expect(200)
        .end(function (err, res) {
          var response = JSON.parse(res.text);
          response.errors.length.should.equal(1);
          response.errors[0].messages.length.should.equal(1);
          response.errors[0].types.length.should.equal(1);
          done();
        });
    });
  });
});