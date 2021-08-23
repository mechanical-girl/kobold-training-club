var listElements = require('./element_lister.js')
var updaterButton = require('./updater-button.js')
// https://stackoverflow.com/questions/23125338/how-do-i-use-browserify-with-external-dependencies
var $ = require('jQuery');
const partyManager = require('./party-manager.js');
const encounterManager = require('./encounter-manager.js')
const sourcesManager = require('./sources-manager.js');
const { floatify } = require('./updater-button.js');

var monsterParameters = {};
var monsterDataTable;
var customSourceNames = [];
var unofficialSourceNames = []

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
        ]
    });
    $.fn.dataTableExt.oSort["cr-desc"] = function (a, b) { return updaterButton.floatify(a) < updaterButton.floatify(b); }
    $.fn.dataTableExt.oSort["cr-asc"] = function (a, b) { return updaterButton.floatify(a) > updaterButton.floatify(b); }
    monsterDataTable.columns.adjust().draw();

    // Populate the character selectors
    partyManager.createCharLevelCombo();

    $.getJSON('/api/unofficialsources').done(function (response) { unofficialSourceNames = response; })

    $(document).on("click", ".party-update", function () {
        partyManager.handleClick(this)
    });

    // Handle sort updates
    $(".updater_button").on("click", function () {
        updaterButton.sortTable();
    })

    $(".toggle_all_button").on("click", function () {
        var listUpdated = updaterButton.AssociatedId(this);
        command = $(this).text()
        console.log(command);
        if (command == "Deselect All") {
            $('#' + listUpdated).find(":input").prop("checked", false)
            $(this).text("Select All");
        } else if (command == "Select All") {
            $('#' + listUpdated).find(":input").prop("checked", true)
            $(this).text("Deselect All");
        }
        monsterDataTable.ajax.reload();
        monsterDataTable.columns.adjust().draw();
    })

    $(document).on("click", "#customSourceFinder .unofficial-source", function () {
        var li = $(this).parent().parent()
        li.detach();
        $('#sources_selector').append(li);
    })

    // Handle monster adds
    $(document).on("click", "#monsterTable > tbody > tr", function () {
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
