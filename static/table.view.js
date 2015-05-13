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
                        $("#info").append("<tr><td><b>Value (" + $("#field_list").val() + ")</b></td><td><b>Count</b></td><td><b>Average Age</b></td></tr>");
                        for (var i = 0; i < data.length; i++) {
                                var field_info = "<tr>";
                                for (var j = 0; j < data[i].length; j++) {
                                    field_info += "<td>" + data[i][j] + "</td>";
                                }
                                field_info += "</tr>";
                                $("#info").append(field_info);
                        } 
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
            var selectedField = $("#field_list").val();
            $("#hidden").empty();
	    $.getJSON(
                $SCRIPT_ROOT + '/_get_hidden_count', { field: selectedField },
                function(data) {
                    $("#hidden").append("<span>Hidden Values: " + data + "</span><br />");
                }
            );

            $.getJSON(
                $SCRIPT_ROOT + '/_get_hidden_row_count', { field: selectedField },
                function(data) {
                    $("#hidden").append("<span>Hidden Row Count: " + data + "</span><br />");
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
