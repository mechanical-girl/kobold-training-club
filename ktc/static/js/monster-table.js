// monster-table.js

var monsterTableFinder = function (callback, parameters) {
    $.post("/api/monsters", { params: JSON.stringify(parameters) }, callback);
}

var monsterTableFormatter = function (monsters) {
    tableString = "";
    for (var i = 0; i < monsters.length; i++) {
        tableString = tableString + '<tr><th scope="row">';
        tableString = tableString + monsters[i]['name'] + '</th><td>';
        tableString = tableString + monsters[i]['cr'] + '</td><td>';
        tableString = tableString + monsters[i]['size'] + '</td><td>';
        tableString = tableString + monsters[i]['type'] + '</td><td>';
        tableString = tableString + monsters[i]['alignment'] + '</td><td>';
        tableString = tableString + monsters[i]['sources'] + '</td></tr>\n';
    }
    return tableString;

};

var monsterTableUpdater = function (monsters) {
    var tableText = monsterTableFormatter(monsters);
    $('#monsterTable tbody').empty();
    $('#monsterTable tbody').append(tableText);
}

var update = function (params = {}) {
    monsterTableFinder(monsterTableUpdater, params);
}

module.exports = { update: update, monsterTableFormatter: monsterTableFormatter, monsterTableUpdater: monsterTableUpdater };