var listElements = require('./element_lister.js')
//https://stackoverflow.com/questions/23125338/how-do-i-use-browserify-with-external-dependencies
var $ = require('jQuery');

$.getJSON("/api/environments", function (data) {

    var parent = $("#environments_selector");
    parent.append(listElements(data, "environment"));

});
