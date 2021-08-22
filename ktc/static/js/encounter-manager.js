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