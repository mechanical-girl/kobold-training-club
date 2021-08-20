var listElements = require('./element_lister.js')
var updaterButton = require('./updater-button.js')
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

    $.getJSON("/api/crs", function (data) {
        var min = $("#challengeRatingMinimum");
        var max = $("#challengeRatingMaximum")
        for (let i = 0; i < data.length; i++) {
            var option = "<option value='" + data[i] + "'>" + data[i] + "</option>"
            min.append(option);
            max.append(option);
        }
    })

    monsterDataTable = $('#monsterTable').DataTable({
        "ajax": {
            "url": '/api/monsters',
            "type": 'POST',
            "data": getMonsterParameters
        }
    });
    monsterDataTable.columns.adjust().draw();
})

$(function () {
    $(".updater_button").on("click", function () {
        var listUpdated = updaterButton.AssociatedId(this);
        if (listUpdated == "maxCr") {
            var values = updaterButton.getUpdatedChallengeRatings();
            monsterParameters["minimumChallengeRating"] = values[0]
            monsterParameters["maximumChallengeRating"] = values[1]
        } else {
            listUpdatedName = listUpdated.split("_")[0];
            monsterParameters[listUpdatedName] = updaterButton.GetUpdatedValues(listUpdated);
        }
        monsterDataTable.ajax.reload();
        monsterDataTable.columns.adjust().draw();
    })
});