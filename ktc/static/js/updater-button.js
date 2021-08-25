// updater-button.js

var AssociatedId = function (clicked_button) {
    if (clicked_button != undefined) {
        attachedParamChooser = $(clicked_button).parent().children("ul")[0];
        if (attachedParamChooser == undefined) {
            attachedParamChooser = $(clicked_button).parent().children("")[0];
        }
        return $(attachedParamChooser).attr('id');
    }
}

var GetUpdatedValues = function (updatedList) {
    if (updatedList != undefined) {
        parent_list = $("#" + updatedList);
        var selected_elements = []
        for (var i = 0; i < parent_list.find("input").length; i++) {
            var this_box = parent_list.find("input")[i];
            if ($(this_box).prop("checked")) {
                selected_elements.push(this_box.id);
            }
        }
        return selected_elements;
    }
}

var floatify = function (number) {
    if (number.includes('/')) {
        var y = number.split('/');
        return (y[0] / y[1]);
    } else {
        return parseInt(number)
    }
}

var getUpdatedChallengeRatings = function () {
    var minValue = $("#minCr option:selected").attr("value");
    var maxValue = $("#maxCr option:selected").attr("value");
    minValueComp = floatify(minValue)
    maxValueComp = floatify(maxValue)
    if (maxValueComp < minValueComp) {
        $("#challengeRatingSelectorDiv").prepend('<div class="alert alert-danger" role="alert">Please ensure your minimum challenge rating is less than or equal to your maximum challenge rating.</div>')
    } else {
        var alerts = $("#challengeRatingSelectorDiv .alert")
        for (var i = 0; i < alerts.length; i++) {
            alerts[i].remove();
        }
    }

    return [minValue, maxValue];
}

var sortTable = function (clicked_button) {
    var listUpdated = AssociatedId(clicked_button);
    if (listUpdated == "minCr") {
        var values = getUpdatedChallengeRatings();
        monsterParameters["minimumChallengeRating"] = values[0]
        monsterParameters["maximumChallengeRating"] = values[1]
    } else {
        listUpdatedName = listUpdated.split("_")[0];
        window.monsterParameters[listUpdatedName] = GetUpdatedValues(listUpdated);
    }
    window.monsterDataTable.ajax.reload();
    window.monsterDataTable.columns.adjust().draw();
}

var toggleAll = function (clicked_button) {
    var listUpdated = AssociatedId(clicked_button);
    command = $(clicked_button).text()
    if (command == "Deselect All") {
        $('#' + listUpdated).find(":input").prop("checked", false)
        $(clicked_button).text("Select All");
    } else if (command == "Select All") {
        $('#' + listUpdated).find(":input").prop("checked", true)
        $(clicked_button).text("Deselect All");
    }
    window.monsterDataTable.ajax.reload();
    window.monsterDataTable.columns.adjust().draw();
}

module.exports = { GetUpdatedValues: GetUpdatedValues, AssociatedId: AssociatedId, getUpdatedChallengeRatings: getUpdatedChallengeRatings, floatify: floatify, sortTable: sortTable, toggleAll: toggleAll }
