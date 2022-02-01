'use strict';

var validation = require('../lib/index')
  , app = require('./app')
  , should = require('should')
  , request = require('supertest');

describe('sending', function () {

  describe('a parameter as string', function () {
    // Expect default values to be set
    it('should return it as Number, as Joi parses it', function (done) {
      request(app)
      .get('/parsing/params/5')
      .expect(200)
      .end(function (err, res) {
        res.body.id.should.equal(5);
        res.body.id.should.not.equal('5');
        done();
      });
    });
  });

  describe('a query parameter as string', function () {
    it('should return it as Number, as Joi parses it', function (done) {
      request(app)
      .get('/parsing/query?id=5')
      .expect(200)
      .end(function (err, res) {
        res.body.id.should.equal(5);
        res.body.id.should.not.equal('5');
        done();
      });
    });
  });

  describe('a body containing a Number', function () {
    it('should return it as Number, as Joi does not alter it', function (done) {
      request(app)
      .post('/parsing/body')
      .send({ id: 5 })
      .expect(200)
      .end(function (err, res) {
        res.body.id.should.equal(5);
        res.body.id.should.not.equal('5');
        done();
      });
    });
  });

  describe('an header as string', function () {
    it('should return it as Number, as Joi parses it', function (done) {
      request(app)
      .get('/parsing/headers')
      .set('id', '5')
      .expect(200)
      .end(function (err, res) {
        res.body.id.should.equal(5);
        res.body.id.should.not.equal('5');
        done();
      });
    });
  });

  describe('a query parameter as string', function () {
    it('should return it as Number, as Joi parses it', function (done) {
      request(app)
      .get('/parsing/cookies')
      .set('Cookie', 'id=5;')
      .expect(200)
      .end(function (err, res) {
        res.body.id.should.equal(5);
        res.body.id.should.not.equal('5');
        done();
      });
    });
  });

});
