var listElements = require('./element_lister.js')
var updaterButton = require('./updater-button.js')
var monsterTable = require("./monster-table.js")
// https://stackoverflow.com/questions/23125338/how-do-i-use-browserify-with-external-dependencies
var $ = require('jQuery');

var monsterParameters = {};
var monsterDataTable;

var getMonsterParameters = function () {
    return {
        params: JSON.stringify(monsterParameters)
    };
}

$(function () {
    selectors = ["environments", "sizes", "types", "alignments", "sources"]
    for (let i = 0; i < selectors.length; i++) {
        let selector = selectors[i]
        $.getJSON("/api/" + selector, function (data) {
            var parent = $("#" + selector + "_selector");
            parent.append(listElements(data, selector));
        });
    };

    monsterDataTable = $('#monsterTable').DataTable({
        "ajax": {
            "url": '/api/monsters',
            "type": 'POST',
            "data": getMonsterParameters
        }
    })
    //monsterTable.update();
})

$(function () {
    $(".updater_button").on("click", function () {
        var listUpdated = updaterButton.AssociatedId(this);
        listUpdatedName = listUpdated.split("_")[0];
        monsterParameters[listUpdatedName] = updaterButton.GetUpdatedValues(listUpdated);
        //monsterTable.update(monsterParameters);
        monsterDataTable.ajax.reload()
    })
});