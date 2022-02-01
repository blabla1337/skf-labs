var Joi = require('joi');

exports.params = {
  params: {
    id: Joi.number().integer().default(77)
  }
};

exports.query = {
  query: {
    id: Joi.number().integer().default(77)
  }
};

exports.body = {
  body: {
    id: Joi.number().integer().default(77)
  }
};

exports.headers = {
  headers: {
    id: Joi.number().integer().default(77)
  }
};

exports.cookies = {
  cookies: {
    id: Joi.number().integer().default(77)
  }
};
