// monster-finder.js

var monsterFinder = function (parameters = []) {
    $.getJSON("/api/monsters?params=[]", function (data) {
        return (data);
    })
}

module.exports = { monsterFinder: monsterFinder, };