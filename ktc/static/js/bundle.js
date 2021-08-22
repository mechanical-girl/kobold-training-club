(function(){function r(e,n,t){function o(i,f){if(!n[i]){if(!e[i]){var c="function"==typeof require&&require;if(!f&&c)return c(i,!0);if(u)return u(i,!0);var a=new Error("Cannot find module '"+i+"'");throw a.code="MODULE_NOT_FOUND",a}var p=n[i]={exports:{}};e[i][0].call(p.exports,function(r){var n=e[i][1][r];return o(n||r)},p,p.exports,r,e,n,t)}return n[i].exports}for(var u="function"==typeof require&&require,i=0;i<t.length;i++)o(t[i]);return o}return r})()({1:[function(require,module,exports){
// element-lister.js
// https://www.rexfeng.com/blog/2014/07/how-to-unit-test-your-js-and-use-it-in-the-browser/

var listElements = function (data, prefix = "") {
    if (prefix != "") {
        prefix = prefix + "_";
    }
    listText = "";
    for (let i = 0; i < data.length; i++) {
        listText += ("<li><label><input type='checkbox' id='" + prefix + data[i] + "'>" + data[i] + "</label></li>");
    };
    return listText;
};

module.exports = listElements

},{}],2:[function(require,module,exports){
// encounter-manager.js

var addMonster = function () {
    var monsterListDiv = $("#monsterList");
    var monsterName = $(this).children("td:first-child").text()
    level_holder = '<div class="charLevelComboSelector d-flex align-items-center" id="' + optionID + '"><i class="bi bi-dash-square-fill party-update" style="size: 125%; margin-right : 25px;"></i><select class="charLevelComboSelector" id="' + optionID + '">' + options + '</select> characters at level <select class="charLevelComboSelector" id="' + optionID + '">' + options + '</select><i class="bi bi-plus-square-fill party-update" style="size: 125%; margin-left: 25px;"></i></div>';
    characterListDiv.append(level_holder);

}
},{}],3:[function(require,module,exports){
(function (global){(function (){
var listElements = require('./element_lister.js')
var updaterButton = require('./updater-button.js')
// https://stackoverflow.com/questions/23125338/how-do-i-use-browserify-with-external-dependencies
var $ = (typeof window !== "undefined" ? window['jQuery'] : typeof global !== "undefined" ? global['jQuery'] : null);
const partyManager = require('./party-manager.js');
const encounterManager = require('./encounter-manager.js')

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

    // Handle monster adds
    $(document).on("click", "#monsterTable > tbody > tr", function () {
        encounterManager.addMonster();
    })
});

}).call(this)}).call(this,typeof global !== "undefined" ? global : typeof self !== "undefined" ? self : typeof window !== "undefined" ? window : {})
},{"./element_lister.js":1,"./encounter-manager.js":2,"./party-manager.js":4,"./updater-button.js":5}],4:[function(require,module,exports){
//party-manager.js

var createCharLevelCombo = function () {
    var characterListDiv = $("#characterList");
    var optionID = $("#characterList div").length

    var options = "";
    for (var i = 1; i <= 20; i++) {
        options += '<option value="' + i + '">' + i + '</option>'
    }
    level_holder = '<div class="charLevelComboSelector d-flex align-items-center" id="' + optionID + '"><i class="bi bi-dash-square-fill party-update" style="size: 125%; margin-right : 25px;"></i><select class="charLevelComboSelector" id="characterNumber' + optionID + '">' + options + '</select> characters at level <select class="charLevelComboSelector" id="levelNumber' + optionID + '">' + options + '</select><i class="bi bi-plus-square-fill party-update" style="size: 125%; margin-left: 25px;"></i></div>';
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

    var party = [];
    var comboSelectorDivs = $("div .charLevelComboSelector");
    for (var i = 0; i <= comboSelectorDivs.length; i++) {
        let selectors = $(comboSelectorDivs[i]).children("select")
        if (selectors.length > 0) {
            party[party.length] = new Array($(selectors[0]).val(), $(selectors[1]).val())
        }
    }
    console.log(party);

    $.ajax({
        type: "POST",
        url: "/api/expthresholds",
        contentType: "application/json",
        data: JSON.stringify(party),
        success: function (result) {
            console.log(result);
        }

    })
};

module.exports = { createCharLevelCombo: createCharLevelCombo, handleClick: handleClick }

},{}],5:[function(require,module,exports){
// updater-button.js

var AssociatedId = function (clicked_button) {
    if (clicked_button != undefined) {
        parent_list = $(clicked_button).prev();
        return parent_list.attr('id');
    }
}

var GetUpdatedValues = function (updatedList) {
    if (updatedList != undefined) {
        parent_list = $("#" + updatedList);
        var selected_elements = []
        for (var i = 0; i < parent_list.children().length; i++) {
            var this_box = parent_list.children()[i].children[0].children[0];
            if ($(this_box).prop("checked")) {
                selected_elements.push(this_box.id);
            }
        }
        console.log(selected_elements);
        return selected_elements;
    }
}

var getUpdatedChallengeRatings = function () {
    var minValue = $("#minCr option:selected").attr("value");
    var maxValue = $("#maxCr option:selected").attr("value");
    if (minValue.includes('/')) {
        var y = minValue.split('/');
        var minValueComp = y[0] / y[1];
    } else {
        var minValueComp = minValue
    }
    if (maxValue.includes('/')) {
        var y = maxValue.split('/');
        var maxValueComp = y[0] / y[1];
    } else {
        var maxValueComp = maxValue
    }
    if (maxValue < minValueComp) {
        $("#challengeRatingSelectorDiv").prepend('<div class="alert alert-danger" role="alert">Please ensure your minimum challenge rating is less than or equal to your maximum challenge rating.</div>')
    } else {
        var alerts = $("#challengeRatingSelectorDiv .alert")
        for (var i = 0; i < alerts.length; i++) {
            alerts[i].remove();
        }
    }

    return [minValue, maxValue];
}

module.exports = { GetUpdatedValues: GetUpdatedValues, AssociatedId: AssociatedId, getUpdatedChallengeRatings: getUpdatedChallengeRatings }

},{}]},{},[3]);
