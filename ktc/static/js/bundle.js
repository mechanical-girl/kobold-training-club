(function(){function r(e,n,t){function o(i,f){if(!n[i]){if(!e[i]){var c="function"==typeof require&&require;if(!f&&c)return c(i,!0);if(u)return u(i,!0);var a=new Error("Cannot find module '"+i+"'");throw a.code="MODULE_NOT_FOUND",a}var p=n[i]={exports:{}};e[i][0].call(p.exports,function(r){var n=e[i][1][r];return o(n||r)},p,p.exports,r,e,n,t)}return n[i].exports}for(var u="function"==typeof require&&require,i=0;i<t.length;i++)o(t[i]);return o}return r})()({1:[function(require,module,exports){
// element-lister.js
// https://www.rexfeng.com/blog/2014/07/how-to-unit-test-your-js-and-use-it-in-the-browser/

var listElements = function (data, prefix = "") {
    if (prefix != "") {
        prefix = prefix + "_";
    }
    listText = "";
    for (let i = 0; i < data.length; i++) {
        listText += ("<li><label><input type='checkbox' id='" + prefix + data[i] + "'>" + data[i] + "</label></li>");
    };
    return listText;
};

module.exports = listElements
},{}],2:[function(require,module,exports){
(function (global){(function (){
var listElements = require('./element_lister.js')
var updaterButtonClicked = require('./updater-button.js')
var monsterTable = require("./monster-table.js")
// https://stackoverflow.com/questions/23125338/how-do-i-use-browserify-with-external-dependencies
var $ = (typeof window !== "undefined" ? window['jQuery'] : typeof global !== "undefined" ? global['jQuery'] : null);

$(function () {
    selectors = ["environments", "sizes", "types", "alignments", "sources"]
    for (let i = 0; i < selectors.length; i++) {
        let selector = selectors[i]
        $.getJSON("/api/" + selector, function (data) {
            var parent = $("#" + selector + "_selector");
            parent.append(listElements(data, selector));
        });
    };

    let monsterTableString = monsterTable.monsterTableFinder(monsterTable.monsterTableUpdater);
})

$(function () {
    $(".updater_button").on("click", function () {
        updaterButtonClicked(this);
    })
});

// Relabel expand and collapse buttons
$(function () {
    $('.expand-collapse').on("click", function () {
        if ($(this).hasClass('glyphicon-chevron-down')) {
            $(this).html('<i class="bi bi-chevron-up"></i> Hide');
        }
        else {
            $(this).html('<i class="bi bi-chevron-down"></i> Show');
        }
    });
})
}).call(this)}).call(this,typeof global !== "undefined" ? global : typeof self !== "undefined" ? self : typeof window !== "undefined" ? window : {})
},{"./element_lister.js":1,"./monster-table.js":3,"./updater-button.js":4}],3:[function(require,module,exports){
// monster-table.js

var monsterTableFinder = function (callback, parameters = []) {
    $.getJSON("/api/monsters", { "params": parameters }, callback);
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
    console.log(tableString);
    return tableString;

};

var monsterTableUpdater = function (monsters) {
    var tableText = monsterTableFormatter(monsters);
    $('#monsterTable tbody').empty();
    $('#monsterTable tbody').append(tableText);
}

module.exports = { monsterTableFinder: monsterTableFinder, monsterTableFormatter: monsterTableFormatter, monsterTableUpdater: monsterTableUpdater };
},{}],4:[function(require,module,exports){
// updater-button.js

var updaterButtonClicked = function (clicked_button) {
    if (clicked_button != undefined) {
        parent_list = $(clicked_button).prev()
        var selected_elements = []
        for (var i = 0; i < parent_list.children().length; i++) {
            var this_box = parent_list.children()[i].children[0].children[0];
            if ($(this_box).prop("checked")) {
                selected_elements.push(this_box.id);
            }
        }
        console.log(selected_elements)
        return selected_elements;
    }
}

module.exports = updaterButtonClicked
},{}]},{},[2]);
