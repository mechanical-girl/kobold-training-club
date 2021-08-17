// updater-button-spec.js
/* jslint node: true */
/* global describe, it, expect */

'use strict';
var updaterButton = require('../ktc/static/js/updater-button.js');

var jsdom = require('jsdom')
var JSDOM = jsdom.JSDOM;

var dom = new JSDOM('\
<!DOCTYPE html>\
<html>\
    <head>\
    </head>\
    <body>\
        <ul id="checkList">\
            <li>\
                <label>\
                    <input type="checkbox" id="first_input">\
                </label>\
            </li>\
            <li>\
                <label>\
                    <input type="checkbox" id="second_input">\
                </label>\
            </li>\
            <li>\
                <label>\
                    <input type="checkbox" id="third_input" checked>\
                </label>\
            </li>\
        </ul>\
        <span class="try_me" id="test_span">\
    </body>\
</html>'
);

var document = dom.window.document;
var window = document.defaultView;
global.$ = require('jquery')(window);

describe("#getUpdatedValues", function () {
    it('should return a list of the ids of checked boxes, given the id of the ul.', function () {
        let expected = ["third_input"]
        let actual = updaterButton.GetUpdatedValues("checkList")
        expect(actual).toEqual(expected);
    })
})