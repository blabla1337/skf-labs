'use strict';

var validation = require('../lib/index')
, app = require('./app')
, should = require('should')
, request = require('supertest');

describe('validate a mixture of request types', function () {

  describe('when the request contains a valid payload and headers', function () {
    
    it('should return a 200 ok response', function (done) {

      var login = {
        email: 'andrew.keig@gmail.com',
        password: '12356'
      };

      request(app)
        .put('/user/1')
        .send(login)
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

  describe('when the request contains a valid payload and headers, with invalid parameter', function () {
    
    it('should return a 200 ok response', function (done) {

      var login = {
        email: 'andrew.keig@gmail.com',
        password: '12356'
      };

      request(app)
        .put('/user/e')
        .send(login)
        .set('accessToken', '4343434343')
        .set('userId', '3243243242')
        .expect(200)
        .end(function (err, res) {
          var response = JSON.parse(res.text);
          response.errors.length.should.equal(1);
          response.errors[0].messages.length.should.equal(1);
          response.errors[0].types.length.should.equal(1);
          response.errors[0].field.should.equal('id');
          done();
        });
    });
  });

  describe('when the request contains a missing payload and valid headers', function () {
    
    it('should return a 400 ok response and two errors', function (done) {

      var login = {
        email: 'andrew.keig@gmail.com',
        password: ''
      };

      request(app)
        .put('/user/1')
        .send(login)
        .set('accessToken', '4343434343')
        .set('userId', '3243243242')
        .expect(400)
        .end(function (err, res) {
          var response = JSON.parse(res.text);
          response.errors.length.should.equal(1);
          response.errors[0].messages.length.should.equal(2);
          response.errors[0].field.should.equal('password');
          done();
        });
    });
  });

  describe('when the request contains a valid payload and missing headers', function () {
    
    it('should return a 400 ok response and two errors', function (done) {

      var login = {
        email: 'andrew.keig@gmail.com',
        password: '32323432'
      };

      request(app)
        .put('/user/1')
        .send(login)
        .set('accesstoken', '')
        .set('userid', '3243243242')
        .expect(400)
        .end(function (err, res) {
          var response = JSON.parse(res.text);
          response.errors.length.should.equal(1);
          response.errors[0].messages.length.should.equal(1);
          response.errors[0].field.should.equal('accesstoken');
          done();
        });
    });
  });
});