// https://github.com/Asmor/5e-monsters/blob/master/app/services/integration.service.js

var generateCombatantPayload = function (monsters, monsterData) {
    var combatants = [];
    monsters.forEach(function (itm) {
        var name = itm[0];
        var qty = itm[1];
        var hp = 0;
        var init = 0;
        var ac = 0;
        var fid = "<unknown>";

        // find more data by name
        for (var itmData of monsterData) {
            if (itmData[0] == name) {
                fid = itmData[8];
                hp = parseInt(itmData[9]);
                ac = parseInt(itmData[10]);
                init = parseInt(itmData[11]);
                break;
            }
        }

        for (var i = 1; i <= qty; i++) {
            combatants.push({
                Name: name,
                HP: { Value: hp },
                TotalInitiativeModifier: init,
                AC: { Value: ac },
                Player: "npc",
                Id: fid,
            });
        }
    });

    return combatants;
}

function openImprovedInitiative(data) {
    var form = document.createElement("form");
    form.style.display = "none";
    form.setAttribute("method", "POST");
    form.setAttribute("action", "https://www.improved-initiative.com/launchencounter/");

    Object.keys(data).forEach(function (key) {
        var textarea = document.createElement("input");
        textarea.setAttribute("type", "hidden");
        textarea.setAttribute("name", key);
        textarea.setAttribute("value", JSON.stringify(data[key]));

        form.appendChild(textarea);
    });

    window.document.body.appendChild(form);
    form.submit();
    form.parentNode.removeChild(form);
}

module.exports = {
    generateCombatantPayload: generateCombatantPayload,
    openImprovedInitiative: openImprovedInitiative
}
