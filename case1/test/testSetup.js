require('@babel/register')();
require('@babel/polyfill');

const path = require('path');
const driversDirPath = path.join(__dirname, 'driver');
process.env.PATH = process.env.PATH + ':' + driversDirPath;
