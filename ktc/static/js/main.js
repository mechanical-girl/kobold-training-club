var listElements = require('./element_lister.js')
var updaterButtonClicked = require('./updater-button.js')
var monsterTable = require("./monster-table.js")
// https://stackoverflow.com/questions/23125338/how-do-i-use-browserify-with-external-dependencies
var $ = require('jQuery');

$(function () {
    selectors = ["environments", "sizes", "types", "alignments", "sources"]
    for (let i = 0; i < selectors.length; i++) {
        let selector = selectors[i]
        $.getJSON("/api/" + selector, function (data) {
            var parent = $("#" + selector + "_selector");
            parent.append(listElements(data, selector));
        });
    };

    let monsterTableString = monsterTable.monsterTableFinder(monsterTable.monsterTableUpdater);
})

$(function () {
    $(".updater_button").on("click", function () {
        updaterButtonClicked(this);
    })
});

// Relabel expand and collapse buttons
$(function () {
    $('.expand-collapse').on("click", function () {
        if ($(this).hasClass('glyphicon-chevron-down')) {
            $(this).html('<i class="bi bi-chevron-up"></i> Hide');
        }
        else {
            $(this).html('<i class="bi bi-chevron-down"></i> Show');
        }
    });
})