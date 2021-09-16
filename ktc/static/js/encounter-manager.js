// encounter-manager.js
var escapeText = function (text) {
    return text.replace(/&/g, '&amp;')
        .replace(/>/g, '&gt;')
        .replace(/</g, '&lt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&apos;');
}

var cr_xp_mapping = {
    "0": 10,
    "1/8": 25,
    "1/4": 50,
    "1/2": 100,
    "1": 200,
    "2": 450,
    "3": 700,
    "4": 1100,
    "5": 1800,
    "6": 2300,
    "7": 2900,
    "8": 3900,
    "9": 5000,
    "10": 5900,
    "11": 7200,
    "12": 8400,
    "13": 10000,
    "14": 11500,
    "15": 13000,
    "16": 15000,
    "17": 18000,
    "18": 20000,
    "19": 22000,
    "20": 25000,
    "21": 33000,
    "22": 41000,
    "23": 50000,
    "24": 62000,
    "25": 75000,
    "26": 90000,
    "27": 105000,
    "28": 120000,
    "29": 135000,
    "30": 155000,
}


var highlight_colours = ["#fff", "#dff0d8", "#f6ce95", "#eba5a3", "#888"]


$(function () {
    $(".exp-list.easy").css("background-color", highlight_colours[0])
    $(".exp-list.medium").css("background-color", highlight_colours[1])
    $(".exp-list.hard").css("background-color", highlight_colours[2])
    $(".exp-list.deadly").css("background-color", highlight_colours[3])
    $(".exp-list.daily").css("background-color", highlight_colours[4])
});

var difficulties = ["easy", "medium", "hard", "deadly", "daily"]

var addMonster = function (cell) {
    var monsterListDiv = $("#monsterList");
    var row = $(cell).parent()
    var monsterName = $(row).children("td:first-child").text()
    var monsterSource = $(row).children("td:last-child").text()
    for (var i = 0; i < $('#monsterList').children('div').length; i++) {
        var monsterDiv = $('#monsterList').children('div')[i]
        if (monsterName == monsterDiv.id) {
            updateMonsterCount($(monsterDiv).children('i')[1]);
            return
        }
    }
    level_holder = '<div class="monsterSelector d-flex align-items-center" id="' + escapeText(monsterName) + '"><i class="bi bi-dash-square-fill encounter-update" style="size: 125%; margin-right : 5px;"></i><span>1</span>x ' + monsterName + '<i class="bi bi-plus-square-fill encounter-update" style="size: 125%; margin-left: 5px;"></i></div>';
    monsterListDiv.append(level_holder);

    updateEncounterDifficulty();
}

var importEncounter = function () {
    var monsters = JSON.parse(window.localStorage.getItem("monsters"));
    var monsterListDiv = $("#monsterList");
    if (monsters != null) {
        for (var i = 0; i < monsters.length; i++) {
            level_holder = '<div class="monsterSelector d-flex align-items-center" id="' + monsters[i][0] + '"><i class="bi bi-dash-square-fill encounter-update" style="size: 125%; margin-right : 5px;"></i><span>' + monsters[i][1] + '</span>x ' + monsters[i][0] + '<i class="bi bi-plus-square-fill encounter-update" style="size: 125%; margin-left: 5px;"></i></div>';
            monsterListDiv.append(level_holder);
        }
    }
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

var highlightEncounterDifficulty = function () {
    $(".exp-list.easy").css("background-color", highlight_colours[0])
    $(".exp-list.medium").css("background-color", highlight_colours[1])
    $(".exp-list.hard").css("background-color", highlight_colours[2])
    $(".exp-list.deadly").css("background-color", highlight_colours[3])
    $(".exp-list.daily").css("background-color", highlight_colours[4])
    for (var i = 0; i < window.partyThresholds.length; i++) {
        if (window.encounterDifficulty < window.partyThresholds[0]) {
            $(".exp-list").css("opacity", "0.7");
            $(".exp-list").css("font-weight", "normal");
        } else if (window.encounterDifficulty > window.partyThresholds[i]) {
            $(".exp-list").css("opacity", "0.7");
            $(".exp-list").css("font-weight", "normal");
            $(".exp-list." + difficulties[i]).css("opacity", "1")
            $(".exp-list." + difficulties[i]).css("font-weight", "bold")
        }
    }
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

    window.localStorage.setItem("monsters", JSON.stringify(monstersInEncounter));

    $.ajax({
        type: "POST",
        url: "api/encounterxp",
        data: { monsters: JSON.stringify(monstersInEncounter) },
        success: function (results) {
            $('#encounterDifficulty').empty();
            $('#encounterDifficulty').text('(' + results + 'XP)')
            window.encounterDifficulty = results;
            highlightEncounterDifficulty()
        }
    })

}

var colourCell = function (cellData) {
    var monsterExp = cr_xp_mapping[cellData];
    if (monsterExp <= window.partyThresholds[0]) {
        return highlight_colours[0]
    } else if (monsterExp >= partyThresholds.slice(-1)) {
        return highlight_colours.slice(-1)
    }
    for (var i = 0; i < window.partyThresholds.length - 1; i++) {
        if (monsterExp >= window.partyThresholds[i] && monsterExp < window.partyThresholds[i + 1]) {
            return highlight_colours[i]
        }
    }
}

var colourAllCells = function () {
    var cells = $("#monsterTable .crCell")
    for (var i = 0; i < cells.length; i++) {
        let cell = cells[i];
        $(cell).css("background-color", colourCell($(cell).text()))
    }
}

module.exports = { addMonster: addMonster, updateMonsterCount: updateMonsterCount, highlightEncounterDifficulty: highlightEncounterDifficulty, importEncounter: importEncounter, colourCell: colourCell, colourAllCells: colourAllCells }