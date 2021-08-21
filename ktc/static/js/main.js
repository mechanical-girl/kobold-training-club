var listElements = require('./element_lister.js')
var updaterButton = require('./updater-button.js')
// https://stackoverflow.com/questions/23125338/how-do-i-use-browserify-with-external-dependencies
var $ = require('jQuery');
const partyManager = require('./party-manager.js');

var monsterParameters = {};
var monsterDataTable;

var getMonsterParameters = function () {
    return {
        params: JSON.stringify(monsterParameters)
    };
}

$(function () {
    // Populate the first five accordions
    selectors = ["environments", "sizes", "types", "alignments", "sources"]
    for (let i = 0; i < selectors.length; i++) {
        let selector = selectors[i]
        $.getJSON("/api/" + selector, function (data) {
            var parent = $("#" + selector + "_selector");
            parent.append(listElements(data, selector));
        });
    };

    // Populate the last accordion
    $.getJSON("/api/crs", function (data) {
        var min = $("#challengeRatingMinimum");
        var max = $("#challengeRatingMaximum")
        for (let i = 0; i < data.length; i++) {
            var option = "<option value='" + data[i] + "'>" + data[i] + "</option>"
            min.append(option);
            max.append(option);
        }
    })

    // Populate the monster table
    monsterDataTable = $('#monsterTable').DataTable({
        "ajax": {
            "url": '/api/monsters',
            "type": 'POST',
            "data": getMonsterParameters
        },
        "columns": [
            { data: 0 },
            {
                data: 1,
                render: function (data, type, row) {
                    if (type === 'sort') {
                        var y = data.split('/');
                        if (y.length > 1) {
                            return (y[0] / y[1]);
                        }
                        else {
                            return (y[0]);
                        }
                    } else {
                        return data
                    }
                }
            },
            { data: 2 },
            { data: 3 },
            { data: 4 },
            { data: 5 }
        ]
    });
    monsterDataTable.columns.adjust().draw();

    // Populate the character selectors
    partyManager.createCharLevelCombo();

    $(document).on("click", ".party-update", function () {
        partyManager.handleClick(this)
    });

    // Handle sort updates
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
