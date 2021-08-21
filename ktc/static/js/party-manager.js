//party-manager.js

var createCharLevelCombo = function () {
    var characterListDiv = $("#characterList");
    var options = '<option value="1">1</option><option value="2">2</option><option value="3">3</option>';
    characterListDiv.append('<select>' + options + '</select>');

    var levelListDiv = $("#levelList");
    levelListDiv.append('<select>' + options + '</select>');
}

module.exports = { createCharLevelCombo: createCharLevelCombo }
