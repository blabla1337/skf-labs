'use strict';

var validation = require('../lib/index');
var app = require('./app');
var request = require('supertest');
require('should');

describe('schema options', function () {

  describe('when schema options does not contain a status options', function () {

    it('should return a 400 ok response and "Bad Request" as message', function (done) {

      var login = {
        email: 'andrew.keiggmail.com',
        password: '12356'
      };

      request(app)
        .post('/login')
        .send(login)
        .expect(400)
        .end(function (err, res) {
          var response = JSON.parse(res.text);
          response.errors.length.should.equal(1);
          response.status.should.equal(400);
          response.statusText.should.equal('Bad Request');
          done();
        });
    });
  });

  describe('when schema options contains a 422 status code', function () {

    it('should return a 422 response', function (done) {

      request(app)
        .post('/options')
        .send('')
        .expect(422)
        .end(function (err, res) {
          var response = JSON.parse(res.text);
          response.errors.length.should.equal(1);
          response.status.should.equal(422);
          response.statusText.should.equal('Unprocessable Entity');
          done();
        });
    });
  });
});

describe('global options', function () {

  describe('when the user globally setups some options', function () {

    it('they should be inherited by every validation instance', function () {

      validation.options({
        status: 422
      });

      var validationFn = validation(require('./validation/login'));
      var fakeReq = {
        body: {
          email: 'andrew.keiggmail.com',
          password: '12356'
        }
      };

      validationFn(fakeReq, undefined, function next (err) {
        err.errors.length.should.equal(1);
        err.status.should.equal(422);
        err.statusText.should.equal('Bad Request');
      });
    });
  });

  describe('when user decides to reset options to default', function () {

    it('should be able to reset options on demand', function () {

      validation.options({
        status: 422
      });

      validation.options();

      var validationFn = validation(require('./validation/login'));
      var fakeReq = {
        body: {
          email: 'andrew.keiggmail.com',
          password: '12356'
        }
      };

      validationFn(fakeReq, undefined, function next (err) {
        err.errors.length.should.equal(1);
        err.status.should.equal(400);
        err.statusText.should.equal('Bad Request');
      });
    });
  });
});
