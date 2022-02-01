'use strict';
require('should');
var app = require('./app');
var request = require('supertest');

describe('validate body', function () {

  describe('when the request contains a valid payload', function () {

    it('should return a 200 ok response', function (done) {

      var login = {
        email: 'andrew.keig@gmail.com',
        password: '12356'
      };

      request(app)
        .post('/login')
        .send(login)
        .expect(200)
        .end(function (err, res) {
          var response = JSON.parse(res.text);
          response.should.equal(200);
          done();
        });
    });
  });

  describe('when the request contains an invalid payload', function () {

    it('should return a 400 response and a single error', function (done) {

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
          done();
        });
    });
  });

  describe('when the request has a missing item in payload', function () {

    it('should return a 400 response and a single error', function (done) {

      var login = {
        email: 'andrew.keig@gmail.com',
        password: ''
      };

      request(app)
        .post('/login')
        .send(login)
        .expect(400)
        .end(function (err, res) {
          var response = JSON.parse(res.text);
          response.errors.length.should.equal(1);
          response.errors[0].messages.length.should.equal(2);
          response.errors[0].types.length.should.equal(2);
          done();
        });
    });
  });

  describe('when the request has multiple missing items in payload', function () {

    it('should return a 400 response and two errors', function (done) {

      var login = {
        email: '',
        password: ''
      };

      request(app)
        .post('/login')
        .send(login)
        .expect(400)
        .end(function (err, res) {
          var response = JSON.parse(res.text);
          response.errors.length.should.equal(2);
          response.errors[0].messages.length.should.equal(2);
          response.errors[0].types.length.should.equal(2);
          response.errors[1].messages.length.should.equal(2);
          response.errors[1].types.length.should.equal(2);
          done();
        });
    });
  });

  describe('when the request has extra items in payload', function () {

    it('should return a 400 response and one error', function (done) {

      var login = {
        email: 'andrew.keig@gmail.com',
        password: '12356',
        token: '1234'
      };

      request(app)
        .post('/login')
        .send(login)
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
