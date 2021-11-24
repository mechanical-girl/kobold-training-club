// sources-manager.js

const listElements = require('./element_lister.js');

var searchSources = function () {
    var searchTerm = $("#customSourceSearcher").val();
    if (searchTerm != undefined) {
        $("#customSourceFinder").empty();
        searchTerm = searchTerm.toLowerCase();
        console.log(window.unofficialSourceNames)
        for (var i = 0; i < window.unofficialSourceNames.length; i++) {
            if (window.unofficialSourceNames[i].toLowerCase().indexOf(searchTerm) != -1) {
                $("#customSourceFinder").append('<li><label><input type="checkbox" class="unofficial-source" id="sources_' + window.unofficialSourceNames[i] + '">' + window.unofficialSourceNames[i] + '</label></li>');
            }
        }
    }
}

var getUnofficialSources = function () {
    $.getJSON('/api/unofficialsources').done(function (response) {
        let unofficialSourceNames = response;
        $("#customSourcesUsed").empty;
        //$("#customSourcesUsed").append(listElements(unofficialSourceNames, "sources"));
        window.unofficialSourceNames = unofficialSourceNames;
    })
}

var moveSourceCheckbox = function (checked_box) {
    if ($("#customSourcesUsed").children("li").length == 0) {
        $("#customSourcesUsed").parent().append('<button class="updater_button">Update</button>')
    }
    var li = $(checked_box).parent().parent()
    li.detach();
    $('#customSourcesUsed').append(li);
}
module.exports = { searchSources: searchSources, moveSourceCheckbox: moveSourceCheckbox, getUnofficialSources: getUnofficialSources }