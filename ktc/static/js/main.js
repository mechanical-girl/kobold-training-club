var listElements = require('./element_lister.js')
var updaterButtonClicked = require('./updater-button.js')
//https://stackoverflow.com/questions/23125338/how-do-i-use-browserify-with-external-dependencies
var $ = require('jQuery');

$(function () {
    selectors = ["environments", "sizes", "types", "alignments", "sources"]
    for (let i = 0; i < selectors.length; i++) {
        let selector = selectors[i]
        $.getJSON("/api/" + selector, function (data) {
            var parent = $("#" + selector + "_selector");
            parent.append(listElements(data, selector));
        })
    }
})

$(function () {
    $(".updater_button").on("click", function () {
        updaterButtonClicked(this);
    })
});