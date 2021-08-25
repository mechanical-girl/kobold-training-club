(function(){function r(e,n,t){function o(i,f){if(!n[i]){if(!e[i]){var c="function"==typeof require&&require;if(!f&&c)return c(i,!0);if(u)return u(i,!0);var a=new Error("Cannot find module '"+i+"'");throw a.code="MODULE_NOT_FOUND",a}var p=n[i]={exports:{}};e[i][0].call(p.exports,function(r){var n=e[i][1][r];return o(n||r)},p,p.exports,r,e,n,t)}return n[i].exports}for(var u="function"==typeof require&&require,i=0;i<t.length;i++)o(t[i]);return o}return r})()({1:[function(require,module,exports){
// element-lister.js
// https://www.rexfeng.com/blog/2014/07/how-to-unit-test-your-js-and-use-it-in-the-browser/

var listElements = function (data, prefix = "") {
    if (prefix != "") {
        prefix = prefix + "_";
    }
    listText = "";
    for (let i = 0; i < data.length; i++) {
        listText += ("<li><label><input type='checkbox' id=\"" + prefix + data[i] + "\" checked>" + data[i] + "</label></li>");
    };
    return listText;
};

module.exports = listElements

},{}],2:[function(require,module,exports){
// encounter-manager.js

var addMonster = function (row) {
    var monsterListDiv = $("#monsterList");
    var monsterName = $(row).children("td:first-child").text()
    var monsterSource = $(row).children("td:last-child").text()
    for (var i = 0; i < $('#monsterList').children('div').length; i++) {
        var monsterDiv = $('#monsterList').children('div')[i]
        if (monsterName == monsterDiv.id) {
            updateMonsterCount($(monsterDiv).children('i')[1]);
            return
        }
    }
    level_holder = '<div class="monsterSelector d-flex align-items-center" id="' + monsterName + '"><i class="bi bi-dash-square-fill encounter-update" style="size: 125%; margin-right : 5px;"></i><span>1</span>x ' + monsterName + '<i class="bi bi-plus-square-fill encounter-update" style="size: 125%; margin-left: 5px;"></i></div>';
    monsterListDiv.append(level_holder);

    updateEncounterDifficulty();
}

var updateMonsterCount = function (clicked_button) {
    if (clicked_button == window.document || clicked_button == undefined) { return }

    var button_classes = clicked_button.className.split(/\s+/);

    if (button_classes.indexOf("encounter-update") == -1) {
        return
    }

    var thisMonsterDiv = $(clicked_button).parent();
    var thisSpan = $(thisMonsterDiv).children('span')[0]
    var noOfMonsters = parseInt($(thisSpan).text())

    if (button_classes.indexOf("bi-plus-square-fill") != -1) {
        $(thisSpan).text(noOfMonsters + 1);
    } else if (button_classes.indexOf("bi-dash-square-fill") != -1) {
        if (noOfMonsters == 1) {
            thisMonsterDiv.remove();
        } else {
            $(thisSpan).text(noOfMonsters - 1);
        }
    }

    updateEncounterDifficulty()
}

var updateEncounterDifficulty = function () {
    var monsterListDiv = $('#monsterList');
    var monstersInEncounter = new Array()
    for (var i = 0; i < $(monsterListDiv).children('div').length; i++) {
        var thisMonsterDiv = $(monsterListDiv).children('div')[i];
        let monsterName = $(monsterListDiv).children('div')[i].id;
        let thisSpan = $($(monsterListDiv).children('div')[i]).children('span')[0]
        let noOfMonsters = parseInt($(thisSpan).text())
        monstersInEncounter[monstersInEncounter.length] = new Array(monsterName, noOfMonsters)
    }

    $.ajax({
        type: "POST",
        url: "api/encounterxp",
        data: { monsters: JSON.stringify(monstersInEncounter) },
        success: function (results) {
            $('#encounterDifficulty').empty();
            $('#encounterDifficulty').text('(' + results + 'XP)')

        }
    })

}
module.exports = { addMonster: addMonster, updateMonsterCount: updateMonsterCount }
},{}],3:[function(require,module,exports){
(function (global){(function (){
const listElements = require('./element_lister.js')
const updaterButton = require('./updater-button.js')
// https://stackoverflow.com/questions/23125338/how-do-i-use-browserify-with-external-dependencies
var $ = (typeof window !== "undefined" ? window['jQuery'] : typeof global !== "undefined" ? global['jQuery'] : null);
const partyManager = require('./party-manager.js');
const encounterManager = require('./encounter-manager.js')
const sourcesManager = require('./sources-manager.js');
window.monsterParameters = {};
window.monsterDataTable;
var customSourceNames = [];
var unofficialSourceNames = []

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
                window.monsterParameters['sources'] = updaterButton.GetUpdatedValues("sources_selector");
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
        ]
    });
    $.fn.dataTableExt.oSort["cr-desc"] = function (a, b) { return updaterButton.floatify(a) < updaterButton.floatify(b); }
    $.fn.dataTableExt.oSort["cr-asc"] = function (a, b) { return updaterButton.floatify(a) > updaterButton.floatify(b); }
    window.monsterDataTable.columns.adjust().draw();

    // Populate the character selectors
    partyManager.createCharLevelCombo();

    $.getJSON('/api/unofficialsources').done(function (response) { unofficialSourceNames = response; })

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
}).call(this)}).call(this,typeof global !== "undefined" ? global : typeof self !== "undefined" ? self : typeof window !== "undefined" ? window : {})
},{"./element_lister.js":1,"./encounter-manager.js":2,"./party-manager.js":4,"./sources-manager.js":5,"./updater-button.js":6}],4:[function(require,module,exports){
//party-manager.js

var createCharLevelCombo = function () {
    var characterListDiv = $("#characterList");
    var optionID = $("#characterList div").length

    var options = "";
    for (var i = 1; i <= 20; i++) {
        options += '<option value="' + i + '">' + i + '</option>'
    }
    level_holder = '<div class="charLevelComboSelector d-flex align-items-center" id="' + optionID + '"><i class="bi bi-dash-square-fill party-update" style="size: 125%; margin-right : 5px;"></i><select class="charLevelComboSelector" id="characterNumber' + optionID + '">' + options + '</select> characters at level <select class="charLevelComboSelector" id="levelNumber' + optionID + '">' + options + '</select><i class="bi bi-plus-square-fill party-update" style="size: 125%; margin-left: 5px;"></i></div>';
    characterListDiv.append(level_holder);
}

var handleClick = function (clicked_button) {
    if (clicked_button == window.document || clicked_button == undefined) { return }

    var button_classes = clicked_button.className.split(/\s+/);

    if (button_classes.indexOf("party-update") == -1) {
        return
    }

    if (button_classes.indexOf("bi-plus-square-fill") != -1) {
        createCharLevelCombo();
    } else if (button_classes.indexOf("bi-dash-square-fill") != -1 && $("#characterList div").length > 1) {
        $(clicked_button).parent().remove();
    }


};

var updateThresholds = function () {
    var party = [];
    var comboSelectorDivs = $("div .charLevelComboSelector");
    for (var i = 0; i <= comboSelectorDivs.length; i++) {
        let selectors = $(comboSelectorDivs[i]).children("select")
        if (selectors.length > 0) {
            party[party.length] = new Array(parseInt($(selectors[0]).val()), parseInt($(selectors[1]).val()))
        }
    }

    $.ajax({
        type: "POST",
        url: "/api/expthresholds",
        data: { party: JSON.stringify(party) },
        success: function (result) {
            var displayDiv = $("div #encounterThresholds");
            displayDiv.empty();
            displayDiv.append('<div class="row float-end"><div class="col">Easy: ' + result[0].toLocaleString("en-GB") + 'exp</div></div>');
            displayDiv.append('<div class="row float-end"><div class="col">Medium: ' + result[1].toLocaleString("en-GB") + 'exp</div></div>');
            displayDiv.append('<div class="row float-end"><div class="col">Hard: ' + result[2].toLocaleString("en-GB") + 'exp</div></div>');
            displayDiv.append('<div class="row float-end"><div class="col">Deadly: ' + result[3].toLocaleString("en-GB") + 'exp</div></div>');
            displayDiv.append('<div class="row float-end"><div class="col">Daily: ' + result[4].toLocaleString("en-GB") + 'exp</div></div>');
        }

    })
}

module.exports = { createCharLevelCombo: createCharLevelCombo, handleClick: handleClick, updateThresholds: updateThresholds }

},{}],5:[function(require,module,exports){
// sources-manager.js

var searchSources = function (unofficialSourceNames) {
    var searchTerm = $("#customSourceSearcher").val();
    if (searchTerm != undefined) {
        $("#customSourceFinder").empty();
        searchTerm = searchTerm.toLowerCase();
        for (var i = 0; i < unofficialSourceNames.length; i++) {
            if (unofficialSourceNames[i].toLowerCase().indexOf(searchTerm) != -1) {
                $("#customSourceFinder").append('<li><label><input type="checkbox" class="unofficial-source" id="sources_' + unofficialSourceNames[i] + '">' + unofficialSourceNames[i] + '</label></li>');
            }
        }
    }
}

var moveSourceCheckbox = function (checked_box) {
    if ($("#customSourcesUsed").children("li").length == 0) {
        $("#customSourcesUsed").parent().append('<button class="updater_button">Update</button>')
    }
    var li = $(checked_box).parent().parent()
    li.detach();
    $('#customSourcesUsed').append(li);
}
module.exports = { searchSources: searchSources, moveSourceCheckbox: moveSourceCheckbox }
},{}],6:[function(require,module,exports){
// updater-button.js

var AssociatedId = function (clicked_button) {
    if (clicked_button != undefined) {
        attachedParamChooser = $(clicked_button).parent().children("ul")[0];
        if (attachedParamChooser == undefined) {
            attachedParamChooser = $(clicked_button).parent().children("")[0];
        }
        return $(attachedParamChooser).attr('id');
    }
}

var GetUpdatedValues = function (updatedList) {
    if (updatedList != undefined) {
        parent_list = $("#" + updatedList);
        var selected_elements = []
        for (var i = 0; i < parent_list.find("input").length; i++) {
            var this_box = parent_list.find("input")[i];
            if ($(this_box).prop("checked")) {
                selected_elements.push(this_box.id);
            }
        }
        return selected_elements;
    }
}

var floatify = function (number) {
    if (number.includes('/')) {
        var y = number.split('/');
        return (y[0] / y[1]);
    } else {
        return parseInt(number)
    }
}

var getUpdatedChallengeRatings = function () {
    var minValue = $("#minCr option:selected").attr("value");
    var maxValue = $("#maxCr option:selected").attr("value");
    minValueComp = floatify(minValue)
    maxValueComp = floatify(maxValue)
    if (maxValueComp < minValueComp) {
        $("#challengeRatingSelectorDiv").prepend('<div class="alert alert-danger" role="alert">Please ensure your minimum challenge rating is less than or equal to your maximum challenge rating.</div>')
    } else {
        var alerts = $("#challengeRatingSelectorDiv .alert")
        for (var i = 0; i < alerts.length; i++) {
            alerts[i].remove();
        }
    }

    return [minValue, maxValue];
}

var sortTable = function (clicked_button) {
    var listUpdated = AssociatedId(clicked_button);
    if (listUpdated == "minCr") {
        var values = getUpdatedChallengeRatings();
        monsterParameters["minimumChallengeRating"] = values[0]
        monsterParameters["maximumChallengeRating"] = values[1]
    } else {
        listUpdatedName = listUpdated.split("_")[0];
        window.monsterParameters[listUpdatedName] = GetUpdatedValues(listUpdated);
    }
    window.monsterDataTable.ajax.reload();
    window.monsterDataTable.columns.adjust().draw();
}

var toggleAll = function (clicked_button) {
    var listUpdated = AssociatedId(clicked_button);
    command = $(clicked_button).text()
    if (command == "Deselect All") {
        $('#' + listUpdated).find(":input").prop("checked", false)
        $(clicked_button).text("Select All");
    } else if (command == "Select All") {
        $('#' + listUpdated).find(":input").prop("checked", true)
        $(clicked_button).text("Deselect All");
    }
    window.monsterDataTable.ajax.reload();
    window.monsterDataTable.columns.adjust().draw();
}

module.exports = { GetUpdatedValues: GetUpdatedValues, AssociatedId: AssociatedId, getUpdatedChallengeRatings: getUpdatedChallengeRatings, floatify: floatify, sortTable: sortTable, toggleAll: toggleAll }

},{}]},{},[3]);
