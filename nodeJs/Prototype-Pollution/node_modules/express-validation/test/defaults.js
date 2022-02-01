'use strict';
require('should');
var app = require('./app');
var request = require('supertest');

describe('set default values', function () {
  describe('when the values are  missing', function () {
  // Expect default values to be set
    it('should return the request with default values', function (done) {
      request(app)
        .post('/defaults')
        .send({ firstname: 'Jane', lastname: 'Doe' })
        .expect(200)
        .end(function (err, res) {
          var response = JSON.parse(res.text);
          response.username.should.equal('jane-doe');
          done();
        });  
    });
  });

});
