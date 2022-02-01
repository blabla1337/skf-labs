'use strict';

var Joi = require('joi');

module.exports = {
  query: {
    q: Joi.string().required()
  }
};