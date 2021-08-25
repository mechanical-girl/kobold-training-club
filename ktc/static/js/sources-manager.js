// sources-manager.js

var searchSources = function (unofficialSourceNames) {
    var searchTerm = $("#customSourceSearcher").val();
    if (searchTerm != undefined) {
        $("#customSourceFinder").empty();
        searchTerm = searchTerm.toLowerCase();
        for (var i = 0; i < unofficialSourceNames.length; i++) {
            if (unofficialSourceNames[i].toLowerCase().indexOf(searchTerm) != -1) {
                $("#customSourceFinder").append('<li><label><input type="checkbox" class="unofficial-source" id="sources_' + unofficialSourceNames[i] + '">' + unofficialSourceNames[i] + '</label></li>');
            }
        }
    }
}

var moveSourceCheckbox = function (checked_box) {
    if ($("#customSourcesUsed").children("li").length == 0) {
        $("#customSourcesUsed").parent().append('<button class="updater_button">Update</button>')
    }
    var li = $(checked_box).parent().parent()
    li.detach();
    $('#customSourcesUsed').append(li);
}
module.exports = { searchSources: searchSources, moveSourceCheckbox: moveSourceCheckbox }