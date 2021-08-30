// element-lister-spec.js
/* jslint node: true */
/* global describe, it, expect */

'use strict';
var listElements = require('../ktc/static/js/element_lister.js');

describe('#listEnvironments', function () {
    it('should wrap each element in the list passed to it in an li with id equal to that element, a label, and an pre-checked input checkbox', function () {
        var expected = "<li><label><input type='checkbox' id=\"aquatic\" checked>aquatic</label></li><li><label><input type='checkbox' id=\"arctic\" checked>arctic</label></li>"//<li id='cave'><label><input type='checkbox'>cave</label></li><li id='coast'><label><input type='checkbox'>coast</label></li><li id='desert'><label><input type='checkbox'>desert</label></li><li id='dungeon'><label><input type='checkbox'>dungeon</label></li><li id='forest'><label><input type='checkbox'>forest</label></li><li id='grassland'><label><input type='checkbox'>grassland</label></li><li id='mountain'><label><input type='checkbox'>mountain</label></li><li id='planar'><label><input type='checkbox'>planar</label></li><li id='ruins'><label><input type='checkbox'>ruins</label></li><li id='swamp'><label><input type='checkbox'>swamp</label></li><li id='underground'><label><input type='checkbox'>underground</label></li><li id='urban'><label><input type='checkbox'>urban</label></li>"

        var list_of_items = ['aquatic', 'arctic',];//'cave', 'coast', 'desert', 'dungeon', 'forest', 'grassland', 'mountain', 'planar', 'ruins', 'swamp', 'underground', 'urban'];

        var actual = listElements(list_of_items);
        expect(expected).toEqual(actual)
    })
})