// element-lister-spec.js
/* jslint node: true */
/* global describe, it, expect */

'use strict';
var listElements = require('../ktc/static/js/element_lister.js');

describe('#listEnvironments', function () {
    it('should wrap each element in the list passed to it in an li with id equal to that element, a label, and an input checkbox', function () {
        var expected = "<li id='aquatic'><label><input type='checkbox'>aquatic</label></li><li id='arctic'><label><input type='checkbox'>arctic</label></li><li id='cave'><label><input type='checkbox'>cave</label></li><li id='coast'><label><input type='checkbox'>coast</label></li><li id='desert'><label><input type='checkbox'>desert</label></li><li id='dungeon'><label><input type='checkbox'>dungeon</label></li><li id='forest'><label><input type='checkbox'>forest</label></li><li id='grassland'><label><input type='checkbox'>grassland</label></li><li id='mountain'><label><input type='checkbox'>mountain</label></li><li id='planar'><label><input type='checkbox'>planar</label></li><li id='ruins'><label><input type='checkbox'>ruins</label></li><li id='swamp'><label><input type='checkbox'>swamp</label></li><li id='underground'><label><input type='checkbox'>underground</label></li><li id='urban'><label><input type='checkbox'>urban</label></li>"

        var list_of_items = ['aquatic', 'arctic', 'cave', 'coast', 'desert', 'dungeon', 'forest',
            'grassland', 'mountain', 'planar', 'ruins', 'swamp', 'underground', 'urban'];

        var actual = listElements(list_of_items);
        expect(actual).toBe(expected);
    })
})

describe('#listEnvironments', function () {
    it('should wrap each element in the list passed to it in an li with an id equal to the prefix passed to it plus an underscore, or none if a prefix is not passed to it, a label, and an input checkbox', function () {
        var expected = "<li id='environment_aquatic'><label><input type='checkbox'>aquatic</label></li><li id='environment_arctic'><label><input type='checkbox'>arctic</label></li><li id='environment_cave'><label><input type='checkbox'>cave</label></li><li id='environment_coast'><label><input type='checkbox'>coast</label></li><li id='environment_desert'><label><input type='checkbox'>desert</label></li><li id='environment_dungeon'><label><input type='checkbox'>dungeon</label></li><li id='environment_forest'><label><input type='checkbox'>forest</label></li><li id='environment_grassland'><label><input type='checkbox'>grassland</label></li><li id='environment_mountain'><label><input type='checkbox'>mountain</label></li><li id='environment_planar'><label><input type='checkbox'>planar</label></li><li id='environment_ruins'><label><input type='checkbox'>ruins</label></li><li id='environment_swamp'><label><input type='checkbox'>swamp</label></li><li id='environment_underground'><label><input type='checkbox'>underground</label></li><li id='environment_urban'><label><input type='checkbox'>urban</label></li>"

        var list_of_items = ['aquatic', 'arctic', 'cave', 'coast', 'desert', 'dungeon', 'forest',
            'grassland', 'mountain', 'planar', 'ruins', 'swamp', 'underground', 'urban'];

        var prefix = "environment";

        var actual = listElements(list_of_items, prefix);
        expect(actual).toBe(expected);
    })
});