'use strict';

var Joi = require('joi');

module.exports = {
  params: {
    id : Joi.number().integer().required()
  }
};