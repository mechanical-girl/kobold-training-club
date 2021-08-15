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