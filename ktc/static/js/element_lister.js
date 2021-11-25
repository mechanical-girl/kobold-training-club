// element-lister.js
// https://www.rexfeng.com/blog/2014/07/how-to-unit-test-your-js-and-use-it-in-the-browser/

var listElements = function (data, prefix = "") {
    if (prefix != "") {
        var stored = window.localStorage.getItem(prefix + "_selector")
        prefix = prefix + "_";
    }
    let listText = "";
    let storeMe = [];
    for (let i = 0; i < data.length; i++) {
        var checked = "";
        if (stored != null && stored.indexOf(data[i]) != -1) {
            checked = " checked"
            listText += ("<li><label><input type='checkbox' id=\"" + prefix + data[i] + "\"" + checked + ">" + data[i] + "</label></li>");
            storeMe.push(data[i]);
        }
    };
    window.localStorage.setItem(prefix + "_selector", storeMe.join(","));
    console.log("storeMe")
    console.log(storeMe.join(","));
    return listText;
};


module.exports = listElements
