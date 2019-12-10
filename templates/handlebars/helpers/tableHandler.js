var Handlebars = require('handlebars');
module.exports = function(data, column) {
    var html = "";

    for (var i = 0; i < column.length; i++) {
        var rowData = data[column[i]];

        rowData = rowData == null ? '' : rowData;

        html += "<td data-value='" + data[column[i]] + "' data-column='" + column[i] + "'>" + rowData + "</td>"
    }

    return new Handlebars.SafeString(html);
};