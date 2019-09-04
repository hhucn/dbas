function AdminGui() {
    'use strict';

    /**
     * Colors text of the element, specified by the class
     *
     * @param _this current scope
     * @param elements_class class of the specific element
     * @param text_class class which should be added
     */
    this.activateElement = function (_this, elements_class, text_class) {
        var element = $(_this).parents('td:first').find('.' + elements_class);
        element.removeClass('text-muted').addClass(text_class);
        element.parent().css('pointer-events', '');
    };

    /**
     * Mute text of the element, specified by the class
     *
     * @param _this current scope
     * @param elements_class class of the specific element
     * @param text_class class which should be removed
     */
    this.deactivateElement = function (_this, elements_class, text_class) {
        var element = $(_this).parents('td:first').find('.' + elements_class);
        element.addClass('text-muted').removeClass(text_class);
        element.parent().css('pointer-events', 'none');
    };

    /**
     * Open a dialog with every column for adding a new row
     */
    this.setAddClickEvent = function () {
        var _this = this;
        $('body').find('.add').each(function () {
            $(this).click(function () {
                var dialog = $('#' + popupConfirmRowDialogId);
                var body = dialog.find('.modal-body');
                body.children().remove();
                body.append($('<span>').addClass('col-sm-5').addClass('lead').text('Column'));
                body.append($('<span>').addClass('col-sm-7').addClass('lead').text('Value'));
                dialog.modal('show');
                dialog.children().eq(0).removeClass('modal-lg');
                dialog.find('.modal-title').text('Add Data');
                $('#data').find('th:not(:last-child)').each(function () {
                    body = _this.createRowForAddModal(body, $(this).text());
                });
                dialog.find('.btn-danger').off('click').click(function () {
                    dialog.modal('hide');
                });
                dialog.find('.btn-success').off('click').click(function () {
                    var data = {};
                    body.find('input').each(function () {
                        data[$(this).data('for')] = $(this).val();
                    });
                    new AdminAjaxHandler().addSomething(data);
                });
            });
        });
    };

    /**
     * Replaces every span with input field in current row
     *
     * @param table: current html table as element
     */
    this.setEditClickEvent = function (table) {
        var _this = this;
        table.find('.pencil').each(function () {
            $(this).click(function () {
                var parent = $(this).parents('tr:first');
                _this.activateElement(this, 'floppy', 'text-success');
                _this.activateElement(this, 'square', 'text-danger');
                _this.deactivateElement(this, 'pencil', 'text-danger');
                parent.find('td:not(:last)').each(function () {
                    $(this).append($('<input>').attr({
                        'class': 'form-control',
                        'placeholder': $(this).text().trim()
                    }).val($(this).text().trim()));
                    $(this).find('span').hide();
                });
            });
        });
    };

    /**
     * Starts ajax request for deleting current row
     *
     * @param table: current html table as element
     */
    this.setDeleteClickEvent = function (table) {
        var _this = this;
        table.find('.trash').each(function () {
            $(this).click(function () {
                var uids = _this.getUids($(this).parents('tr:first'));
                new AdminAjaxHandler().deleteSomething(uids, $(this).parents('tr:first'));
            });
        });
    };

    /**
     * Starts ajax request for saving edits of current row
     *
     * @param table: current html table as element
     */
    this.setSaveClickEvent = function (table) {
        var _this = this;
        table.find('.floppy').each(function () {
            $(this).click(function () {
                var tmp = $(this).parents('tr:first');
                var uids = _this.getUids(tmp);
                var keys = [];
                var values = [];
                tmp.find('input').each(function () {
                    values.push($(this).val());
                });
                $('#data').find('thead').find('th:not(:last-child)').each(function () {
                    keys.push($(this).text());
                });
                new AdminAjaxHandler().updateSomething(this, uids, keys, values);
                tmp.find('input').remove();
                tmp.find('span').show();
            });
        });
    };

    /**
     * Restores the inital state of the row
     *
     * @param table: current html table as element
     */
    this.setCancelClickEvent = function (table) {
        var _this = this;
        table.find('.square').each(function () {
            $(this).click(function () {
                var tmp = $(this).parents('tr:first');
                _this.deactivateElement(this, 'floppy', 'text-success');
                _this.deactivateElement(this, 'square', 'text-danger');
                _this.activateElement(this, 'pencil', '');
                tmp.find('input').remove();
                tmp.find('span').show();
            });
        });
    };

    /**
     * Searches the PK of the table and returns an array
     *
     * @param element is the tr element of the table
     * @returns {Array}
     */
    this.getUids = function (element) {
        var uids = [];
        // Premise has two columns as PK
        if ($('#table_name').text().toLowerCase() === 'premise') {
            uids.push(parseInt(element.find('td:nth-child(1)').text().trim()));
            uids.push(parseInt(element.find('td:nth-child(2)').text().trim()));
        } else {
            uids.push(parseInt(element.find('td:first').text().trim()));
        }
        return uids;
    };

    /**
     * Creates a row for the 'add-data' modal view
     * @returns {*|jQuery} body element of the modal view
     */
    this.createRowForAddModal = function (body, column) {
        // skip columns, that we do not need!
        if ($.inArray(column, ['uid', 'last_action', 'last_login', 'registered', 'public_nickname']) !== -1) {
            return body;
        }
        var form = $('<div>').addClass('form-group');
        var label = $('<label>')
            .addClass('col-sm-5')
            .addClass('control-label')
            .attr('for', column)
            .text(column);
        var div = $('<div>')
            .addClass('col-sm-7')
            .append($('<input>').attr({
                'class': 'form-control',
                'data-for': column
            }));
        form.append(label).append(div);
        body.append(form);
        return body;
    };
}

// main function
$(document).ready(function () {
    'use strict';

    $('#admin-login-button').click(function () {
        new AjaxLoginHandler().login($('#admin-login-user').val(), $('#admin-login-pw').val(), true);
    });

    var data = $('#data');
    var gui = new AdminGui();

    // events for edit, delete, save, cancel, add
    gui.setEditClickEvent(data);
    gui.setDeleteClickEvent(data);
    gui.setSaveClickEvent(data);
    gui.setCancelClickEvent(data);
    gui.setAddClickEvent();

    try {
        var dict = getLanguage() === 'de' ? dataTables_german_lang : dataTables_english_lang;
        var options = {
            language: dict,
            ordering: true
        };
        if ($('#table_name') === 'History') {
            options.ordering = false;
        }
        data.DataTable(options);
    } catch (e) {
    }
});
