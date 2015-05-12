var TableViewer = {};

$(document).ready(function() {
    TableViewer.fields = (function() {

        /**
         * Displays all table columns in a dropdown
         */
        var displayFields = function() {
            $.getJSON(
                $SCRIPT_ROOT + '/_get_fields', {},
                function(data) {
                    for (var i = 0; i < data.length; i++) {
                        var selected = "";
                        if (i == 0) {
                            selected = "selected=\"selected\"";
                        }
                        $("#field_list").append("<option value=\"" + data[i] + "\"" + selected + ">" + data[i] +"</option>");
                    }
                }
            );
        };

        /**
         * When a field is selected, displays information for that variable. In this case
         * it includes the value, the row count and the average age.
         */
        var selectField = function() {
            $("#field_list").change(function () {
                $("#info").empty();
                insertMissingRowCount();
                $.getJSON(
                    $SCRIPT_ROOT + '/_query_info', { field: $("#field_list").val() },
                    function(data) {
                        nullCount = 0;
                        $("#info").append("<tr><td><b>Value</b></td><td><b>Count</b></td><td><b>Average Age</b></td></tr>");
                        for (var i = 0; i < data.length; i++) {
                            if (data[i][0] === null) {
                                nullCount += data[i][1];
                            } else {
                                var field_info = "<tr>";
                                for (var j = 0; j < data[i].length; j++) {
                                    field_info += "<td>" + data[i][j] + "</td>";
                                }
                                field_info += "</tr>";
                                $("#info").append(field_info);
                            }
                        }
                        $("#info").append("<tr><td>Null Value Row Count (clipped):</td><td>" + nullCount + "</td></tr>");
                    }
                );
            })
            .change();
        };

        /**
         * Shows the number of hidden values (if the different types of values for
         * the variable exceeds 100)
         */
        var insertMissingRowCount = function() {
            $.getJSON(
                $SCRIPT_ROOT + '/_get_variable_count', { field: $("#field_list").val() },
                function(data) {
                    $("#info").append("<tr><td>Hidden Values:</td><td>" + data + "</td></tr>");
                }
            );
        };

        return {
            displayFields: displayFields,
            selectField: selectField
        };
    })();

    TableViewer.fields.displayFields();
    TableViewer.fields.selectField();
});