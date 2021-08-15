(function(){function r(e,n,t){function o(i,f){if(!n[i]){if(!e[i]){var c="function"==typeof require&&require;if(!f&&c)return c(i,!0);if(u)return u(i,!0);var a=new Error("Cannot find module '"+i+"'");throw a.code="MODULE_NOT_FOUND",a}var p=n[i]={exports:{}};e[i][0].call(p.exports,function(r){var n=e[i][1][r];return o(n||r)},p,p.exports,r,e,n,t)}return n[i].exports}for(var u="function"==typeof require&&require,i=0;i<t.length;i++)o(t[i]);return o}return r})()({1:[function(require,module,exports){
// element-lister.js
// https://www.rexfeng.com/blog/2014/07/how-to-unit-test-your-js-and-use-it-in-the-browser/
var listElements = function (data, prefix = "") {
    if (prefix != "") {
        prefix = prefix + "_";
    }
    listText = "";
    for (let i = 0; i < data.length; i++) {
        listText += ("<li id='" + prefix + data[i] + "'><label><input type='checkbox'>" + data[i] + "</label></li>");
    };
    return listText;
};

module.exports = listElements
},{}],2:[function(require,module,exports){
(function (global){(function (){
var listElements = require('./element_lister.js')
//https://stackoverflow.com/questions/23125338/how-do-i-use-browserify-with-external-dependencies
var $ = (typeof window !== "undefined" ? window['jQuery'] : typeof global !== "undefined" ? global['jQuery'] : null);

$.getJSON("/api/environments", function (data) {

    var parent = $("#environments_selector");
    parent.append(listElements(data, "environment"));

});

}).call(this)}).call(this,typeof global !== "undefined" ? global : typeof self !== "undefined" ? self : typeof window !== "undefined" ? window : {})
},{"./element_lister.js":1}]},{},[2]);
