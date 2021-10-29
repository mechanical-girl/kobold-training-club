//party-manager.js

const encounterManager = require("./encounter-manager");

var createCharLevelCombo = function (char, level) {
    var char = (char != undefined) ? char : 1;
    var level = (char != undefined) ? level : 1;
    var characterListDiv = $("#characterList");
    var optionID = $("#characterList div").length;

    var char_options = ""
    var level_options = ""
    for (var i = 1; i <= 20; i++) {
        var selected = (char == i) ? " selected=\"selected\"" : ""
        char_options += '<option value="' + i + '"' + selected + '>' + i + '</option>'
    }
    for (var i = 1; i <= 20; i++) {
        var selected = (level == i) ? " selected=\"selected\"" : ""
        level_options += '<option value="' + i + '"' + selected + '>' + i + '</option>'
    }
    level_holder = '<div class="charLevelComboSelector d-flex align-items-center" id="' + optionID + '"><i class="bi bi-dash-square-fill party-update" style="size: 125%; margin-right : 5px;"></i><select class="charLevelComboSelector" id="characterNumber' + optionID + '">' + char_options + '</select> characters at level <select class="charLevelComboSelector" id="levelNumber' + optionID + '">' + level_options + '</select><i class="bi bi-plus-square-fill party-update" style="size: 125%; margin-left: 5px;"></i></div>';
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

    updateThresholds();
};

var getParty = function() {
    var party = [];
    var comboSelectorDivs = $("div .charLevelComboSelector");
    for (var i = 0; i <= comboSelectorDivs.length; i++) {
        let selectors = $(comboSelectorDivs[i]).children("select")
        if (selectors.length > 0) {
            party[party.length] = new Array(parseInt($(selectors[0]).val()), parseInt($(selectors[1]).val()))
        }
    }

    return party
}

var updateThresholds = function () {
    let party = getParty();


    window.localStorage.setItem("party", JSON.stringify(party))

    $.ajax({
        type: "POST",
        url: "/api/expthresholds",
        data: { party: JSON.stringify(party) },
        success: function (result) {
            var displayDiv = $("div #encounterThresholds");
            displayDiv.empty();
            displayDiv.append('<div class="row float-end"><div class="col exp-list easy">Easy: ' + result[0].toLocaleString("en-GB") + 'exp</div></div>');
            displayDiv.append('<div class="row float-end"><div class="col exp-list medium">Medium: ' + result[1].toLocaleString("en-GB") + 'exp</div></div>');
            displayDiv.append('<div class="row float-end"><div class="col exp-list hard">Hard: ' + result[2].toLocaleString("en-GB") + 'exp</div></div>');
            displayDiv.append('<div class="row float-end"><div class="col exp-list deadly">Deadly: ' + result[3].toLocaleString("en-GB") + 'exp</div></div>');
            displayDiv.append('<div class="row float-end"><div class="col exp-list daily">Daily: ' + result[4].toLocaleString("en-GB") + 'exp</div></div>');
            window.partyThresholds = result;
            encounterManager.highlightEncounterDifficulty();
            encounterManager.colourAllCells();
        }

    })

}

module.exports = { createCharLevelCombo: createCharLevelCombo, handleClick: handleClick, updateThresholds: updateThresholds, getParty: getParty }
