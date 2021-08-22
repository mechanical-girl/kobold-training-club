// encounter-manager.js

var addMonster = function (row) {
    var monsterListDiv = $("#monsterList");
    console.log($(row))
    var monsterName = $(row).children("td:first-child").text()
    level_holder = '<div class="charLevelComboSelector d-flex align-items-center" id="' + monsterName + '"><i class="bi bi-dash-square-fill party-update" style="size: 125%; margin-right : 5px;"></i>' + monsterName + '<i class="bi bi-plus-square-fill party-update" style="size: 125%; margin-left: 5px;"></i></div>';
    monsterListDiv.append(level_holder);

}

module.exports = { addMonster: addMonster }