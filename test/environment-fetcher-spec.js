// environment-fetcher-spec.js

'use strict';
var expect = require('chai').expect;

describe('EnvironmentFetcher', function () {
    it('should exist', function () {
        var EnvironmentFetcher = require('../app/static/environment-fetcher.js');
        expect(EnvironmentFetcher).to.not.be.undefined;
    });
});