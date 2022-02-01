'use strict';

var Joi = require('joi');

module.exports = {
  options: { contextRequest: true },
  body: {
    id: Joi.string().valid(Joi.ref('$params.id')).required()
  }
};
