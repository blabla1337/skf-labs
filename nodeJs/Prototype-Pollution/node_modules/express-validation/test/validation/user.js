'use strict';

var Joi = require('joi');

module.exports.get = {
  headers: {
    accesstoken: Joi.string().required(),
    userid : Joi.string().required()
  }
};

module.exports.put = {
  headers: {
    accesstoken: Joi.string().required(),
    userid : Joi.string().required()
  },
  params: {
    id : Joi.number().integer().required()
  },
  body: {
    email: Joi.string().email().required(),
    password: Joi.string().regex(/[a-zA-Z0-9]{3,30}/).required()
  }
};
