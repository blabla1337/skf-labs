'use strict';
require('should');
var validation = require('../lib/index');

describe('when library throws an error', function () {

  it('should call next() with a ValidationError', function () {
    var validationHandler = validation(require('./validation/login'));
    var fakeReq = {
      body: {
        email: 'andrew.keiggmail.com',
        password: '12356'
      }
    };

    validationHandler(fakeReq, undefined, function next (err) {
      err.should.be.instanceof(validation.ValidationError);
      err.errors.length.should.equal(1);
      err.status.should.equal(400);
      err.statusText.should.equal('Bad Request');
    });
  });

  it('should be compatible with javascript Error', function () {
    var validationHandler = validation(require('./validation/login'));
    var fakeReq = {
      body: {
        email: 'andrew.keiggmail.com',
        password: '12356'
      }
    };

    validationHandler(fakeReq, undefined, function next (err) {
      err.should.be.instanceof(Error);
      err.errors.length.should.equal(1);
      err.status.should.equal(400);
      err.statusText.should.equal('Bad Request');
    });
  });

  it('should not have a stack trace, since is not a coding error', function () {
    var validationHandler = validation(require('./validation/login'));
    var fakeReq = {
      body: {
        email: 'andrew.keiggmail.com',
        password: '12356'
      }
    };

    validationHandler(fakeReq, undefined, function next (err) {
      err.should.not.have.keys('stack');
      err.errors.length.should.equal(1);
      err.status.should.equal(400);
      err.statusText.should.equal('Bad Request');
    });
  });
});
