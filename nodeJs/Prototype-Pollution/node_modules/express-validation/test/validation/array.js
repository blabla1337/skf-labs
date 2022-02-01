var Joi = require('joi');


module.exports = {
  body: {
    numbers: Joi.array().items(Joi.number().valid([1, 2, 3, 4, 5])),
    validate_numbers: Joi.array().items(Joi.number().valid(Joi.ref('$numbers')))
  }
};
