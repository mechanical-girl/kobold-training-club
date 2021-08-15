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
        return selected_elements
    }
}

module.exports = updaterButtonClicked