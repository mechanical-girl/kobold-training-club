// element-lister.js
// https://www.rexfeng.com/blog/2014/07/how-to-unit-test-your-js-and-use-it-in-the-browser/

var listElements = function (data, prefix = "") {
    if (prefix != "") {
        prefix = prefix + "_";
    }
    listText = "";
    for (let i = 0; i < data.length; i++) {
        listText += ("<li><label><input type='checkbox' id='" + prefix + data[i] + "' checked>" + data[i] + "</label></li>");
    };
    return listText;
};

module.exports = listElements
