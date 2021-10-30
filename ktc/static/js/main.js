require('requirish')._(module);
// https://stackoverflow.com/questions/23125338/how-do-i-use-browserify-with-external-dependencies
var $ = require('jQuery');
const listElements = require('./element_lister.js');
const updaterButton = require('./updater-button.js');
const partyManager = require('./party-manager.js');
const encounterManager = require('./encounter-manager.js');
const sourcesManager = require('./sources-manager.js');
const improvedInitiativeService = require('./improved-initiative-service.js');
window.monsterParameters = {};
window.monsterDataTable;
window.partyThresholds = []
window.encounterDifficulty = 0
var customSourceNames = [];
var unofficialSourceNames = []

var getMonsterParameters = function () {
    return {
        params: JSON.stringify(window.monsterParameters)
    };
}
var createMonsterTable = function () {
    // Populate the monster table

    window.monsterDataTable = $('#monsterTable').DataTable({
        "ajax": {
            "url": '/api/monsters',
            "type": 'POST',
            "data": getMonsterParameters
        },
        "aoColumns": [
            {
                "bSortable": true,
                "sType": "name"
            },
            {
                "bSortable": true,
                "sType": "cr",
            },
            { "bSortable": true },
            { "bSortable": true },
            { "bSortable": false },
            { "bSortable": false },
            { "bSortable": true },
            { "bSortable": true },
            { "bSortable": false },
            { "bSortable": false },
            { "bSortable": false },
            { "bSortable": false },
        ],
        "columnDefs": [
            {
                "targets": [0, 1, 2, 3, 4],
                "className": "not-a-link",
            },
            {
                "targets": 1,
                "createdCell": function (td, cellData, rowData, row, col) {
                    $(td).css('background-color', encounterManager.colourCell(cellData));
                    $(td).attr("class", "crCell not-a-link");
                }
            },
            {
                "targets": [4, 5],
                "visible": false,
            },
            {
                "targets": [8, 9, 10, 11],
                "className": "invisibleColumn"
            }
        ],
        "order": [[0, "asc"]]

    });
    $.fn.dataTableExt.oSort["cr-desc"] = function (a, b) {
        a = updaterButton.floatify(a);
        b = updaterButton.floatify(b);
        return ((a < b) ? -1 : ((a > b) ? 1 : 0));
    }
    $.fn.dataTableExt.oSort["cr-asc"] = function (a, b) {
        a = updaterButton.floatify(a);
        b = updaterButton.floatify(b);
        return ((a > b) ? -1 : ((a < b) ? 1 : 0));
    }
    $.fn.dataTableExt.oSort["name-desc"] = function (a, b) { return b.localeCompare(a) }
    $.fn.dataTableExt.oSort["name-asc"] = function (a, b) { return a.localeCompare(b) }
    window.monsterDataTable.columns.adjust().draw();
    //$("input").each($(this).attr({"autocomplete": "off", "autocorrect": "off", "autocapitalize": "off", "spellcheck": "false", color: "pink"}));
}
$(function () {
    // Show any alerts if neede
    let versionNumber = $("#version-number").text().slice(1);
    if (window.localStorage.getItem('lastVersion') != versionNumber && $("#patchNotesModal .modal-body").text().length > 20) {
        window.localStorage.setItem('lastVersion', versionNumber)
        $('#patchNotesModal').modal('show')
    }

    // Populate the first five accordions
    var listPopulatorPromises = []
    selectors = ["sources", "environments", "sizes", "types", "alignments"]
    for (let i = 0; i < selectors.length; i++) {
        let selector = selectors[i];
        listPopulatorPromises.push($.getJSON("/api/" + selector, function (data) {
            var parent = $("#" + selector + "_selector");
            parent.append(listElements(data, selector));
            if (selector == "sources") {
                // Populate unofficial sources
                sourcesManager.getUnofficialSources();
            }
            window.monsterParameters[selector] = data
            console.log(window.monsterParameters)
        }));
    };


    // Populate the last accordion
    listPopulatorPromises.push($.getJSON("/api/crs", function (data) {
        var min = $("#challengeRatingMinimum");
        var max = $("#challengeRatingMaximum");
        let min_cr_stored = JSON.parse(window.localStorage.getItem("minCr"))
        let max_cr_stored = JSON.parse(window.localStorage.getItem("maxCr"))
        let allowNamed = JSON.parse(window.localStorage.getItem("allowNamed"))
        let allowLegendary = JSON.parse(window.localStorage.getItem("allowLegendary"))
        if (min_cr_stored == null) {
            min_cr_stored = data[0]
            max_cr_stored = data.slice(-1)
        }
        for (let i = 0; i < data.length; i++) {
            var standard = "<option value='" + data[i] + "'>" + data[i] + "</option>"
            if (data[i] == min_cr_stored) {
                min.append("<option value='" + data[i] + "' selected> " + data[i] + "</option>")
            } else {
                min.append(standard)
            }
            if (data[i] == max_cr_stored) {
                max.append("<option value='" + data[i] + "' selected> " + data[i] + "</option>")
            } else {
                max.append(standard)
            }

        }

        $("#allowLegendary").prop("checked", true)
        $("#allowNamed").prop("checked", true)
        if (allowLegendary != null && allowLegendary) {
            $("#allowLegendary").prop("checked", true)
        }
        if (allowNamed == false) {
            $("#allowNamed").prop("checked", false)
        }

        updaterButton.sortTable($("#challengeRatingSelectorDiv .updater_button"));


        table = $("#monsterTable").DataTable();
        table.on('draw', function () {
            encounterManager.colourAllCells();
        })

    }))

    $.when(listPopulatorPromises).done(function () {
        console.log(window.monsterParameters)
        createMonsterTable()
        // Populate the character selectors
        var party = JSON.parse(window.localStorage.getItem("party"));
        if (party != null) {
            for (var i = 0; i < party.length; i++) {
                partyManager.createCharLevelCombo(party[i][0], party[i][1]);
            }
        } else {
            partyManager.createCharLevelCombo();
        }
        partyManager.updateThresholds();
        encounterManager.importEncounter();

        $(document).on("click", "#updatesNotesModal .close", function () {
            $("#updatesNotesModal").modal('hide');
        })
        $(document).on("click", ".party-update", function () {
            partyManager.handleClick(this)
        });
        // Handle Improved Initiative button clicks
        $(document).on("click", "#run_in_ii_button", function () {
            var monsters = JSON.parse(window.localStorage.getItem("monsters"));
            var monsterData = window.monsterDataTable.data().toArray()

            var combatants = improvedInitiativeService.generateCombatantPayload(monsters, monsterData)

            improvedInitiativeService.openImprovedInitiative({ Combatants: combatants });
        })
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

        // Handle random encounter generation
        $(document).on("click", "#generate-encounter-button", function() {
            console.log("Generating encounter...");
            let encounterParameters = window.monsterParameters;
            encounterParameters["party"] = partyManager.getParty()
            encounterParameters["difficulty"] = $("#generate-encounter-button").text().split(' ')[0].toLowerCase()
            console.log(encounterParameters)
            encounterManager.generateEncounter(encounterParameters);
        })

        // Handle random encounter difficulty selection
        $(document).on("click", ".random-encounter-difficulty", function() {
            let selectedId = $(this).attr('id');
            let buttonLabel = selectedId.charAt(0).toUpperCase() + selectedId.slice(1) + " Encounter";
            $("#generate-encounter-button").text(buttonLabel);

        })

        $(document).on("input", "#customSourceSearcher", function () {
            sourcesManager.searchSources(unofficialSourceNames);
        })

        $(document).on("input", "#sourceKeyInput", function () {
            $('#sourceKeyManagementDiv .alert').remove();
            key = $("#sourceKeyInput").val()
            if (key == "") { return }
            $('#sourceKeyManagementDiv .alert').remove();
            $('#sourceKeyManagementDiv').prepend('<div class="alert alert-primary" id="processing-custom-source-alert role="alert">Requesting the sheet now...</div >')
            var checkIfSheetProcessed = $.ajax({ type: "POST", url: "/api/checksource", data: { key: JSON.stringify(key) } });
            checkIfSheetProcessed.done(function (data) {
                if (data == "") {
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
                            $('#sourceKeyManagementDiv').prepend('<div class="alert alert-danger" id="processing-custom-source-alert" role="alert">Processing on this sheet failed. Please check that it\'s valid. If you\'re sure it is, please open an issue on Github.</div >')
                        })
                    })
                    customSourceSheetRequest.fail(function (jqXHR, textStatus, errorThrown) {
                        $('#sourceKeyManagementDiv .alert').remove();
                        $('#sourceKeyManagementDiv').prepend('<div class="alert alert-danger" role="alert">Error: ' + jqXHR.status + '.\n If you\'re sure the sheet exists, please open an issue on Github.</div >')
                    });
                } else {
                    $('#sourceKeyManagementDiv .alert').remove();
                    $('#sourceKeyManagementDiv').prepend('<div class="alert alert-primary" id="processing-custom-source-alert role="alert">Source ' + data + ' processed! Search for it in the box above.</div >')

                }
            })

        })

    })
})