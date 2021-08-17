// updater-button.js

var AssociatedId = function (clicked_button) {
    if (clicked_button != undefined) {
        parent_list = $(clicked_button).prev();
        return parent_list.attr('id');
    }
}

var GetUpdatedValues = function (updatedList) {
    if (updatedList != undefined) {
        parent_list = $("#" + updatedList);
        var selected_elements = []
        for (var i = 0; i < parent_list.children().length; i++) {
            var this_box = parent_list.children()[i].children[0].children[0];
            if ($(this_box).prop("checked")) {
                selected_elements.push(this_box.id);
            }
        }
        console.log(selected_elements);
        return selected_elements;
    }
}

module.exports = { GetUpdatedValues: GetUpdatedValues, AssociatedId: AssociatedId }