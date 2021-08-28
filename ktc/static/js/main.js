const listElements = require('./element_lister.js')
const updaterButton = require('./updater-button.js')
// https://stackoverflow.com/questions/23125338/how-do-i-use-browserify-with-external-dependencies
var $ = require('jQuery');
const partyManager = require('./party-manager.js');
const encounterManager = require('./encounter-manager.js')
const sourcesManager = require('./sources-manager.js');
window.monsterParameters = {};
window.monsterDataTable;
window.partyThresholds = []
window.encounterDifficulty = 0
var customSourceNames = [];
var unofficialSourceNames = []
const storage = window.localStorage;

var getMonsterParameters = function () {
    return {
        params: JSON.stringify(window.monsterParameters)
    };
}

$(function () {
    // Populate the first five accordions
    selectors = ["sources", "environments", "sizes", "types", "alignments"]
    for (let i = 0; i < selectors.length; i++) {
        let selector = selectors[i]
        $.getJSON("/api/" + selector, function (data) {
            var parent = $("#" + selector + "_selector");
            parent.append(listElements(data, selector));
            if (selector == "sources") {
                // Populate unofficial sources
                sourcesManager.getUnofficialSources();
            }
        });
    }

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
        "aoColumns": [
            { "bSortable": true },
            {
                "bSortable": true,
                "sType": "cr",
            },
            { "bSortable": true },
            { "bSortable": true },
            { "bSortable": true },
            { "bSortable": true }
        ],
        "columnDefs": [
            { className: "not-a-link", "targets": [0, 1, 2, 3, 4] }
        ]
    });
    $.fn.dataTableExt.oSort["cr-desc"] = function (a, b) { return updaterButton.floatify(a) < updaterButton.floatify(b); }
    $.fn.dataTableExt.oSort["cr-asc"] = function (a, b) { return updaterButton.floatify(a) > updaterButton.floatify(b); }
    window.monsterDataTable.columns.adjust().draw();

    // Populate the character selectors
    var party = JSON.parse(window.localStorage.getItem("party"));
    if (party != null) {
        for (var i = 0; i < party.length; i++) {
            console.log(party[i])
            partyManager.createCharLevelCombo(party[i][0], party[i][1]);
        }
    } else {
        partyManager.createCharLevelCombo();
    }
    partyManager.updateThresholds();

    encounterManager.importEncounter();


    $(document).on("click", ".party-update", function () {
        partyManager.handleClick(this)
    });

    // Handle sort updates
    $(document).on("click", ".updater_button", function () {
        updaterButton.sortTable(this);
    })

    $(".toggle_all_button").on("click", function () {
        updaterButton.toggleAll(this);
    })

    $(document).on("click", "#customSourceFinder .unofficial-source", function () {
        sourcesManager.moveSourceCheckbox(this);
    })

    // Handle monster adds
    $(document).on("click", "#monsterTable > tbody > tr > .not-a-link", function () {
        encounterManager.addMonster(this);
    })

    $(document).on("click", ".encounter-update", function () {
        encounterManager.updateMonsterCount(this);
    })

    $(document).on("change", "select", function () {
        partyManager.updateThresholds();
    })


    $(document).on("input", "#customSourceSearcher", function () {
        sourcesManager.searchSources(unofficialSourceNames);
    })

    $(document).on("input", "#sourceKeyInput", function () {
        key = $("#sourceKeyInput").val()
        $('#sourceKeyManagementDiv .alert').remove();
        $('#sourceKeyManagementDiv').prepend('<div class="alert alert-primary" id="processing-custom-source-alert role="alert">Requesting the sheet now...</div >')
        var customSourceSheetRequest = $.get('https://docs.google.com/spreadsheet/pub?key=' + key + '&output=csv');
        customSourceSheetRequest.done(function (data) {
            $('#sourceKeyManagementDiv .alert').remove();
            $('#sourceKeyManagementDiv').prepend('<div class="alert alert-primary" id="processing-custom-source-alert role="alert">Sheet received. Processing the sheet now...</div >')
            var customSheetProcessRequest = $.ajax({
                type: "POST",
                url: "api/processCSV",
                data: { csv: JSON.stringify(data), key: JSON.stringify(key) },
            })
            customSheetProcessRequest.done(function (results) {
                customSourceNames[customSourceNames.length] = results["name"];
                $('#sourceKeyManagementDiv .alert').remove();
                $('#sourceKeyManagementDiv').prepend('<div class="alert alert-primary" id="processing-custom-source-alert role="alert">Source ' + results['name'] + ' processed! Search for it in the box above.</div >')
                $.getJSON('/api/unofficialsources').done(function (response) { unofficialSourceNames = response; })
            })
            customSheetProcessRequest.fail(function () {
                $('#sourceKeyManagementDiv .alert').remove();
                $('#sourceKeyManagementDiv').prepend('<div class="alert alert-danger" id="processing-custom-source-alert role="alert">Processing on this sheet failed. Please check that it\'s valid. If you\'re sure it is, please open an issue on Github.</div >')
            })
        })
        customSourceSheetRequest.fail(function (jqXHR, textStatus, errorThrown) {
            $('#sourceKeyManagementDiv .alert').remove();
            $('#sourceKeyManagementDiv').prepend('<div class="alert alert-danger" role="alert">Error: ' + jqXHR.status + '.\n If you\'re sure the sheet exists, please open an issue on Github.</div >')
        });
    })
})