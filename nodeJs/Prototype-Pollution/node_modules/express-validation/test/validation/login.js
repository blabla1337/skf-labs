'use strict';

var Joi = require('joi');

module.exports = {
  options: { allowUnknownBody: false },
  body: {
    email: Joi.string().email().required(),
    password: Joi.string().regex(/[a-zA-Z0-9]{3,30}/).required()
  }
};
