// updater-button.js

var AssociatedId = function (clicked_button) {
    if (clicked_button != undefined) {
        console.log($(clicked_button).parent());
        attachedParamChooser = $(clicked_button).parent().children("ul")[0];
        console.log(attachedParamChooser);
        if (attachedParamChooser == undefined) {
            attachedParamChooser = $(clicked_button).parent().children("")[0];
        }
        console.log(attachedParamChooser);
        return $(attachedParamChooser).attr('id');
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

var getUpdatedChallengeRatings = function () {
    var minValue = $("#minCr option:selected").attr("value");
    var maxValue = $("#maxCr option:selected").attr("value");
    if (minValue.includes('/')) {
        var y = minValue.split('/');
        var minValueComp = y[0] / y[1];
    } else {
        var minValueComp = minValue
    }
    if (maxValue.includes('/')) {
        var y = maxValue.split('/');
        var maxValueComp = y[0] / y[1];
    } else {
        var maxValueComp = maxValue
    }
    if (maxValue < minValueComp) {
        $("#challengeRatingSelectorDiv").prepend('<div class="alert alert-danger" role="alert">Please ensure your minimum challenge rating is less than or equal to your maximum challenge rating.</div>')
    } else {
        var alerts = $("#challengeRatingSelectorDiv .alert")
        for (var i = 0; i < alerts.length; i++) {
            alerts[i].remove();
        }
    }

    return [minValue, maxValue];
}

module.exports = { GetUpdatedValues: GetUpdatedValues, AssociatedId: AssociatedId, getUpdatedChallengeRatings: getUpdatedChallengeRatings }
