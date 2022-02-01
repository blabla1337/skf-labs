'use strict';
var Joi = require('joi');

module.exports.post = {
  options: { flatten: true },
  body: {
    email: Joi.string().required().email(),
    password: Joi.string().required().min(6).max(10)
  }
};