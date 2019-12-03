require('./../css/general.css');
require('./../css/dashboard.css');
require('./../library/fontawesome/fontawesome.js');

var createQueryTemplate = require('./../handlebars/query/create_query.hbs');
var tableStepTemplate = require('./../handlebars/query/table_step.hbs');
var columnStepTemplate = require('./../handlebars/query/column_step.hbs');
var queryTableTemplate = require('./../handlebars/query/query_table.hbs');
var queryItemTemplate = require('./../handlebars/query/query_item.hbs');
var databaseWrapperTemplate = require('./../handlebars/query/database_wrapper.hbs');

var $ = require('jquery');

$(document).ready(function() {
    addQuerySideBar(globals.queries);

    var queryId = localStorage.getItem('clicked_query');

    if (queryId === null) {
        var $queryItem = $('.query-item')[0];
        $queryItem.click();
    } else {
        $queryItem = $('.query-item[data-id="' + queryId + '"]');
        $queryItem.click();
    }
});

function addQuerySideBar(queries) {
    var $querySideWrapper = $('#query-side-wrapper');
    $querySideWrapper.empty();

    for (var i = 0; i < queries.length; i++) {
        var currentQuery = queries[i];
        var currentDatabase = currentQuery['database'].replace(/[^A-Za-z]/g, '');
        var $sideDatabaseWrapper = $('.' + currentDatabase + '-list');

        if(!$sideDatabaseWrapper.length) {
            $querySideWrapper.append(databaseWrapperTemplate({'database': currentDatabase}));
        }

        $sideDatabaseWrapper = $('.' + currentDatabase + '-list');
        $sideDatabaseWrapper.append(queryItemTemplate(currentQuery));
    }
}

function sendRequest(url, data, request_type, success, error, exception) {
    $.ajax({
        headers: {"X-CSRFToken": $('input[name="csrfmiddlewaretoken"]').attr('value')},
        url: globals.base_url + url,
        data: data,
        dataType: 'json',
        type: request_type,
        success: function (response) {
            success(response, exception);
        },
        error: function (response) {
            error(response, exception);
        }
    });
}

function overlayError(response) {
    if(response.status && response.status == 403) {
        $('#overlay').find('.error').text(' - Permission Denied').show();
    } else {
        $('#overlay').find('.error').text(' - ' + response.responseText).show();
    }
}

function popupHandler(e, popupData, template) {
    e.stopPropagation();
    var $overlay = $('#overlay');
    $overlay.empty();
    $overlay.addClass('active');
    if(template) {
        $overlay.append(template(popupData));
    }
}

$(document).on('click', '#account-link', function () {
    $(this).closest('#nav-wrapper').toggleClass('account-active');
});

$(document).on('click', '#logout-link', function () {
    window.location.replace(globals.base_url + '/logout');
});

//POPUP//
$(document).on('click', 'body, #cancel-submit, #exit-button', function () {
    $('#overlay').removeClass('active');
});

$(document).on('click', '#overlay', function (e) {
    e.stopPropagation();
});

$(document).on('click', '.next-step', function () {
    var $popup = $('.popup');
    var $this = $(this);

    //SHOW NEXT STEP
    if($this.attr('data-step')) {
        var $nextStep = $('#' + $this.attr('data-step'));
        $nextStep.show();
    }

    var width = $popup.width();

    if($this.attr('data-number')) {
        width = width * parseInt($this.attr('data-number'));
    }

    $popup.animate({scrollLeft: width}, "slow");
});

$(document).on('click', '.prev-step', function () {
    var $popup = $('.popup');
    var $this = $(this);
    var width = $popup.width();

    if($this.attr('data-number')) {
        width = width * parseInt($this.attr('data-number'));
    }

    $popup.animate({scrollLeft: -width}, "slow", function() {})
});
//POPUP//

//QUERY//
$(document).on('click', '#create-query-button', function (e) {
    popupHandler(e, {'database': globals.database}, createQueryTemplate);
});

$(document).on('click', '.database', function () {
    var $this = $(this);
    var data = JSON.stringify({
        'database_name': $this.attr('data-database'),
        'tables': $this.attr('data-tables').split(',')
    });

    function success(response) {
        //console.log(JSON.stringify(response));

        var $tableWrapper = $('#table-wrapper');
        $tableWrapper.empty();

        $.each(response['tables'], function(key, value) {
            var $createdHtml = $(tableStepTemplate({table_name: key, columns: value}));
            $createdHtml.data('data', {'database_name': response['database_name'], 'table_name': key, 'columns': response['tables']});
            $tableWrapper.append($createdHtml);
        });
    }

    sendRequest('/database/table_columns/', data, 'POST', success, overlayError);
});

$(document).on('click', '.table', function () {
    var $this = $(this);

    var data = JSON.stringify($this.data('data'));

    function success(response) {
        //console.log(JSON.stringify(response));

        var $columnWrapper = $('#column-wrapper');
        $columnWrapper.empty();
        $columnWrapper.append(columnStepTemplate(response));

        $('#query-submit').data('relationship_map', response['relationship_map'])
    }

    sendRequest('/database/relationship_map/', data, 'POST', success, overlayError);
});

$(document).on('click', '.include-input', function () {
    var $includeInput = $(this);
    var $importTable = $includeInput.closest('.import-table');
    var columnPosition = (parseInt($includeInput.attr('data-column')) + 1).toString();
    var $columnData = $importTable.find('tbody tr td:nth-child(' + columnPosition + ')');

    $columnData.each(function() {
        if($includeInput.prop('checked')) {
            $(this).addClass('included');
        } else {
            $(this).removeClass('included');
        }
    });
});

$(document).on('click', '#query-submit', function () {
    var $importTable = $('.import-table');
    var column = [];
    var query = {};

    //GET HEADERS
    $importTable.each(function() {
        var $table = $(this);
        var tableName = $table.attr('data-table');
        query[tableName] = {};

        $table.find('.include-input:checked').each(function() {
            var $includeInput = $(this);
            var columnPosition = parseInt($includeInput.attr('data-column'));
            var $columnInput = $table.find('.header-input[data-column="' + columnPosition + '"]');
            var origValue = $columnInput.attr('data-orig_value');
            query[tableName][origValue] = $columnInput.val();
        });
    });

    var data = JSON.stringify({
        'database_name': $importTable.attr('data-database'),
        'query': query,
        'table_name': $importTable.attr('data-selected_table'),
        'relationship_map': $(this).data('relationship_map')
    });

    function success(response) {
        //console.log(JSON.stringify(response));

        var $tableWrapper = $('#query-table-wrapper');
        $tableWrapper.empty();
        $tableWrapper.append(queryTableTemplate(response));

        //APPEND TO SIDE BAR
        addQuerySideBar(response['queries']);

        $('.query-item[data-id="' + response['id'] + '"]').addClass('active');

        $('#overlay').removeClass('active');
    }

    sendRequest('/database/create_query/', data, 'POST', success, overlayError);
});

$(document).on('click', '.query-item', function () {
    var data = {
        'id': $(this).attr('data-id')
    };

    function success(response) {
        console.log(JSON.stringify(response));

        var $tableWrapper = $('#query-table-wrapper');
        $tableWrapper.empty();
        $tableWrapper.append(queryTableTemplate(response));

        localStorage.setItem("clicked_query", String(response['id']));
        $('#query-side-wrapper').find('.active').removeClass('active');
        $('.query-item[data-id="' + response['id'] + '"]').addClass('active');
    }

    sendRequest('/database/get_query/', data, 'GET', success, overlayError);
});

$(document).on('click', '.edit-query-button', function (e) {
    e.stopPropagation();
    alert('Hang on! Feature yet to be added!');
});
//QUERY//