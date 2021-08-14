// environment-fetcher-spec.js

'use strict';
var expect = require('chai').expect;
var EnvironmentFetcher = require('../app/static/js/environment-fetcher.js');

describe('EnvironmentFetcher', function () {
    it('should exist', function () {
        expect(EnvironmentFetcher).to.not.be.undefined;
    });
});

describe('#fetchEnvironments()', function () {
    it('should fetch a list of environments from Flask and return a list', function () {
        var expected = ["aquatic", "arctic", "cave", "coast", "dungeon", "forest", "grassland", "mountain", "planar", "ruins", "swamp", "underground"]
        var actual = EnvironmentFetcher.fetchEnvironments();
        expect(actual).to.eql(expected);
    })
})