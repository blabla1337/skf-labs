'use strict';

var express = require('express');
var validate = require('../lib/index');
var http = require('http');
var validation = require('./validation');
var bodyParser = require('body-parser');
var cookieParser = require('cookie-parser');
var app = express();

app.use(bodyParser.json());
app.use(cookieParser());

app.set('port', 3000);

// generates a response function sending back to user the specified req[key]
function respondWith (key) {
  return function (req, res) {
    res.json(req[key]);
  };
}

function respond200 (req, res) {
  res.json(200);
}

app.post('/login', validate(validation.login), respond200);
app.get('/user', validate(validation.user.get), respond200);
app.get('/search', validate(validation.search), respond200);
app.put('/user/:id', validate(validation.user.put), respond200);
app.post('/register', validate(validation.register.post), respond200);
app.post('/options', validate(validation.options), respond200);
app.get('/account/:id', validate(validation.account), respondWith('params'));
app.post('/defaults', validate(validation.defaults), respondWith('body'));

app.get('/parsing/params/:id?', validate(validation.parsing.params), respondWith('params'));
app.get('/parsing/query', validate(validation.parsing.query), respondWith('query'));
app.post('/parsing/body', validate(validation.parsing.body), respondWith('body'));
app.get('/parsing/headers', validate(validation.parsing.headers), respondWith('headers'));
app.get('/parsing/cookies', validate(validation.parsing.cookies), respondWith('cookies'));

app.post('/logout', validate(validation.logout), respond200);
app.post('/array', validate(validation.array), respond200);
app.post('/context/:id', validate(validation.context), respond200);

// default errorhandler for express-validation
app.use(function (err, req, res, next) {
  res.status(400).json(err);
});

http.createServer(app);
module.exports = app;
