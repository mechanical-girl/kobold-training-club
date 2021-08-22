// encounter-manager.js

var addMonster = function () {
    var monsterListDiv = $("#monsterList");
    var monsterName = $(this).children("td:first-child").text()
    level_holder = '<div class="charLevelComboSelector d-flex align-items-center" id="' + optionID + '"><i class="bi bi-dash-square-fill party-update" style="size: 125%; margin-right : 25px;"></i><select class="charLevelComboSelector" id="' + optionID + '">' + options + '</select> characters at level <select class="charLevelComboSelector" id="' + optionID + '">' + options + '</select><i class="bi bi-plus-square-fill party-update" style="size: 125%; margin-left: 25px;"></i></div>';
    characterListDiv.append(level_holder);

}