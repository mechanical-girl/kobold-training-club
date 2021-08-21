//party-manager.js

var createCharLevelCombo = function () {
    var characterListDiv = $("#characterList");
    var optionID = $("#characterList div").length

    var options = "";
    for (var i = 1; i <= 20; i++) {
        options += '<option value="' + i + '">' + i + '</option>'
    }
    level_holder = '<div class="charLevelComboSelector d-flex align-items-center" id="' + optionID + '"><i class="bi bi-dash-square-fill party-update" style="size: 125%; margin-right : 25px;"></i><select class="charLevelComboSelector" id="' + optionID + '">' + options + '</select> characters at level <select class="charLevelComboSelector" id="' + optionID + '">' + options + '</select><i class="bi bi-plus-square-fill party-update" style="size: 125%; margin-left: 25px;"></i></div>';
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

}

module.exports = { createCharLevelCombo: createCharLevelCombo, handleClick: handleClick }
