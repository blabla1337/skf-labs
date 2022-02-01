'use strict';
require('should');
var app = require('./app');
var request = require('supertest');

describe('validate cookies', function () {

  describe('when the request contains a valid payload', function () {

    it('should return a 200 ok response', function (done) {

      request(app)
        .post('/logout')
        .set('Cookie', 'id=1; session=0123456789abcdef;')
        .send()
        .expect(200)
        .end(function (err, res) {
          var response = JSON.parse(res.text);
          response.should.equal(200);
          done();
        });
    });
  });

  describe('when the request contains an invalid payload', function () {

    it('should return a 400 ok response and a single error', function (done) {

      request(app)
        .post('/logout')
        .set('Cookie', 'id=1; session=abc;')
        .send()
        .expect(400)
        .end(function (err, res) {
          var response = JSON.parse(res.text);
          response.errors.length.should.equal(1);
          done();
        });
    });
  });

  describe('when the request has a missing item in payload', function () {

    it('should return a 400 ok response and a single error', function (done) {

      request(app)
        .post('/logout')
        .set('Cookie', 'id=1;')
        .send()
        .expect(400)
        .end(function (err, res) {
          var response = JSON.parse(res.text);
          response.errors.length.should.equal(1);
          response.errors[0].messages.length.should.equal(1);
          response.errors[0].types.length.should.equal(1);
          done();
        });
    });
  });

  describe('when the request has multiple missing items in payload', function () {

    it('should return a 400 ok response and two errors', function (done) {

      request(app)
        .post('/login')
        .send()
        .expect(400)
        .end(function (err, res) {
          var response = JSON.parse(res.text);
          response.errors.length.should.equal(2);
          response.errors[0].messages.length.should.equal(1);
          response.errors[0].types.length.should.equal(1);
          response.errors[1].messages.length.should.equal(1);
          response.errors[1].types.length.should.equal(1);
          done();
        });
    });
  });

  describe('when the request has extra items in payload', function () {

    it('should return a 400 ok response and one error', function (done) {

      request(app)
        .post('/logout')
        .set('Cookie', 'id=1; session=0123456789abcdef; a=b;')
        .send()
        .expect(400)
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
