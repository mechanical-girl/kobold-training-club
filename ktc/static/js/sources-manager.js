// sources-manager.js

var searchSources = function (unofficialSourceNames) {
    var searchTerm = $("#customSourceSearcher").val();
    console.log(searchTerm);
    if (searchTerm != undefined) {
        $("#customSourceFinder").empty();
        searchTerm = searchTerm.toLowerCase();
        console.log(searchTerm);
        for (var i = 0; i < unofficialSourceNames.length; i++) {
            console.log(unofficialSourceNames[i])
            if (unofficialSourceNames[i].toLowerCase().indexOf(searchTerm) != -1) {
                console.log(unofficialSourceNames[i]);
                $("#customSourceFinder").append('<li><label><input type="checkbox" class="unofficial-source" id="sources_' + unofficialSourceNames[i] + '">' + unofficialSourceNames[i] + '</label></li>');
            }
        }
    }
}
module.exports = { searchSources: searchSources }