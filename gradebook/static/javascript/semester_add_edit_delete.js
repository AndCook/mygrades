$(document).ready(function() {
    var semwrap = $('#semester_squares_wrapper');
    ////////////////////// adding semesters //////////////////////
    var add_semester_form = $('#add_semester_form');
    var add_semester_name = $('#add_semester_name');
    var add_semester_form_is_validated = false;
    add_semester_form.jqxValidator({
        focus: false,
        rules: [
            { input: add_semester_name, message: 'Name is required', action: 'keyup, blur', rule: 'required' }
        ],
        onError: function() {add_semester_form_is_validated = false;},
        onSuccess: function() {add_semester_form_is_validated = true;}
    });
    var add_semester_start_date_button = $('#add_semester_start_date');
    var add_semester_end_date_button = $('#add_semester_end_date');
    add_semester_start_date_button.datepicker({
        changeMonth: true,
        changeYear: true,
        dateFormat: 'M d, yy',
        numberOfMonths: 2,
        minDate: '-6Y',
        maxDate: '+6Y',
        showOn: 'button',
        buttonText: getDateFormatted(),
        showAnim: 'slideDown',
        onClose: function( selectedDate ) {
            if (selectedDate !== '')
                add_semester_start_date_button.datepicker('option', 'buttonText', selectedDate);
            var end_date = Date.parse(add_semester_end_date_button.val());
            var start_date = Date.parse(selectedDate);
            if (start_date > end_date) {
                add_semester_end_date_button.val(selectedDate);
                add_semester_end_date_button.datepicker('option', 'buttonText', selectedDate);
            }
        }
    });
    add_semester_end_date_button.datepicker({
        changeMonth: true,
        changeYear: true,
        dateFormat: 'M d, yy',
        numberOfMonths: 2,
        minDate: '-6Y',
        maxDate: '+6Y',
        showOn: 'button',
        buttonText: getDateFormatted(),
        showAnim: 'slideDown',
        onClose: function( selectedDate ) {
            if (selectedDate !== '')
                add_semester_end_date_button.datepicker('option', 'buttonText', selectedDate);
            var start_date = Date.parse(add_semester_start_date_button.val());
            var end_date = Date.parse(selectedDate);
            if (start_date > end_date) {
                add_semester_start_date_button.val(selectedDate);
                add_semester_start_date_button.datepicker('option', 'buttonText', selectedDate);
            }
        }
    });
    function getDateFormatted() {
        var currentTime = new Date();
        var day = currentTime.getDate();
        var year = currentTime.getFullYear();
        switch (currentTime.getMonth() + 1) {
            case 1: return 'Jan ' + day + ', ' + year;
            case 2: return 'Feb ' + day + ', ' + year;
            case 3: return 'Mar ' + day + ', ' + year;
            case 4: return 'Apr ' + day + ', ' + year;
            case 5: return 'May ' + day + ', ' + year;
            case 6: return 'Jun ' + day + ', ' + year;
            case 7: return 'Jul ' + day + ', ' + year;
            case 8: return 'Aug ' + day + ', ' + year;
            case 9: return 'Sep ' + day + ', ' + year;
            case 10: return 'Oct ' + day + ', ' + year;
            case 11: return 'Nov ' + day + ', ' + year;
            case 12: return 'Dec ' + day + ', ' + year;
            default: return '';
        }
    }
    var add_semester_dialog = $('#add_semester_dialog_box');
    $('#add_semester_button').click(function() {
        add_semester_start_date_button.val(add_semester_start_date_button.datepicker('option', 'buttonText'));
        add_semester_end_date_button.val(add_semester_end_date_button.datepicker('option', 'buttonText'));
        add_semester_dialog.dialog('open');
    });
	add_semester_dialog.dialog({
		autoOpen: false,
		width: 350,
        resizable: false,
		modal: true,
		buttons: {
			'Add Semester': {
                text: 'Add Semester',
                click: function() {
                    add_semester_form.jqxValidator('validate');
                    if (!add_semester_form_is_validated)
                        return;

                    var semester_name = add_semester_name.val();
                    var start_date = add_semester_start_date_button.val();
                    var end_date = add_semester_end_date_button.val();

                    $.ajax({
                        type:"POST",
                        url: "/gradebook/overview/",
                        contentType: "application/x-www-form-urlencoded",
                        data: {
                            'post_action': 'add_semester',
                            'semester_name': semester_name,
                            'start_date': start_date,
                            'end_date': end_date
                        },
                        success: function(data) {
                            add_semester_dialog.dialog('close');
                            $('#add_semester_button').before(data);
                        }
                    });
                }
	      	},
		  	Cancel: function() {
	  			add_semester_dialog.dialog('close')
		  	}
        },
        close: function() {
            // clear course form contents
            add_semester_name.val('');
            add_semester_start_date_button.val(getDateFormatted());
            add_semester_start_date_button.datepicker('option', 'buttonText', getDateFormatted());
            add_semester_start_date_button.datepicker('option', 'minDate', '-6Y');
            add_semester_start_date_button.datepicker('option', 'maxDate', '+6Y');
            add_semester_end_date_button.val(getDateFormatted());
            add_semester_end_date_button.datepicker('option', 'buttonText', getDateFormatted());
            add_semester_end_date_button.datepicker('option', 'minDate', '-6Y');
            add_semester_end_date_button.datepicker('option', 'maxDate', '+6Y');
            // clear any visible validators
            add_semester_form.jqxValidator('hide');
        }
	});
    ////////////////////// renaming semesters //////////////////////
    var rename_semester_dialog = $('#rename_semester_dialog_box');
    var rename_semester_form = $('#rename_semester_form');
    var rename_semester_name = $('#rename_semester_name');
    var rename_semester_form_is_validated = false;
    rename_semester_form.jqxValidator({
        focus: false,
        rules: [
            { input: rename_semester_name, message: 'Name is required', action: 'keyup, blur', rule: 'required' }
        ],
        onError: function() {rename_semester_form_is_validated = false;},
        onSuccess: function() {rename_semester_form_is_validated = true;}
    });
    var semester_id;
    semwrap.on('click', '.s_s_rename', function() {
        semester_id = $(this).closest('.large_semester_square').attr('id').split("_").pop();
        var semester_name = $(this).closest('.s_s_name_div').find('.s_s_name').text().trim();
        rename_semester_dialog.find('#rename_semester_name').val(semester_name);
        rename_semester_dialog.dialog('open');
    });
	rename_semester_dialog.dialog({
		autoOpen: false,
		width: 350,
        resizable: false,
		modal: true,
		buttons: {
			'Rename Semester': {
                text: 'Save',
                click: function() {
                    rename_semester_form.jqxValidator('validate');
                    if (!rename_semester_form_is_validated)
                        return;

                    var new_name = rename_semester_name.val();

                    $.ajax({
                        type:"POST",
                        url: "/gradebook/overview/",
                        contentType: "application/x-www-form-urlencoded",
                        data: {
                            'post_action': 'rename_semester',
                            'semester_id': semester_id,
                            'new_semester_name': new_name
                        },
                        success: function() {
                            rename_semester_dialog.dialog('close');
                            $('#semester_' + semester_id).find('.s_s_name').text(new_name);
                            $('#semester_' + semester_id + '.large_semester_square').find('.s_s_name').text(new_name);
                        }
                    });
                }
	      	},
		  	Cancel: function() {
	  			rename_semester_dialog.dialog('close');
		  	}
        },
        close: function() {
            rename_semester_form.jqxValidator('hide');
        }
	});
    ////////////////////// deleting semesters //////////////////////
    var delete_semester_dialog = $('#delete_semester_dialog_box');
    semwrap.on('click', '.s_s_delete', function() {
        semester_id = $(this).closest('.large_semester_square').attr('id').split("_").pop();
        var semester_name = $(this).closest('.s_s_name_div').find('.s_s_name').text().trim();
        delete_semester_dialog.find('#semester_name').text(semester_name);
        delete_semester_dialog.dialog('open');
    });
    delete_semester_dialog.dialog({
		autoOpen: false,
		width: 350,
        resizable: false,
		modal: true,
		buttons: {
			'Delete Semester': {
                text: 'Delete',
                click: function() {
                    $.ajax({
                        type:"POST",
                        url: "/gradebook/overview/",
                        contentType: "application/x-www-form-urlencoded",
                        data: {
                            'post_action': 'delete_semester',
                            'semester_id': semester_id
                        },
                        success: function() {
                            delete_semester_dialog.dialog('close');
                            $('#semester_' + semester_id).remove();
                            $('#overlay').click();
                        }
                    });
                }
	      	},
		  	Cancel: function() {
	  			delete_semester_dialog.dialog('close');
		  	}
        },
        close: function() {}
	});
    ////////////////////// changing semester dates //////////////////////
    var change_dates_start_date_button = $('#change_dates_start_date');
    var change_dates_end_date_button = $('#change_dates_end_date');
    change_dates_start_date_button.datepicker({
        changeMonth: true,
        changeYear: true,
        dateFormat: 'M d, yy',
        numberOfMonths: 2,
        minDate: '-6Y',
        maxDate: '+6Y',
        showOn: 'button',
        buttonText: getDateFormatted(),
        showAnim: 'slideDown',
        onClose: function( selectedDate ) {
            if (selectedDate !== '')
                change_dates_start_date_button.datepicker('option', 'buttonText', selectedDate);
            var end_date = Date.parse(change_dates_end_date_button.val());
            var start_date = Date.parse(selectedDate);
            if (start_date > end_date) {
                change_dates_end_date_button.val(selectedDate);
                change_dates_end_date_button.datepicker('option', 'buttonText', selectedDate);
            }
        }
    });
    change_dates_end_date_button.datepicker({
        changeMonth: true,
        changeYear: true,
        dateFormat: 'M d, yy',
        numberOfMonths: 2,
        minDate: '-6Y',
        maxDate: '+6Y',
        showOn: 'button',
        buttonText: getDateFormatted(),
        showAnim: 'slideDown',
        onClose: function( selectedDate ) {
            if (selectedDate !== '')
                change_dates_end_date_button.datepicker('option', 'buttonText', selectedDate);
            var start_date = Date.parse(change_dates_start_date_button.val());
            var end_date = Date.parse(selectedDate);
            if (start_date > end_date) {
                change_dates_start_date_button.val(selectedDate);
                change_dates_start_date_button.datepicker('option', 'buttonText', selectedDate);
            }
        }
    });
    var change_dates_dialog = $('#change_dates_dialog_box');
    semwrap.on('click', '.s_s_change_dates', function() {
        semester_id = $(this).closest('.large_semester_square').attr('id').split("_").pop();
        var semester_name = $(this).closest('.large_semester_square').find('.s_s_name').text().trim();
        change_dates_dialog.find('#semester_name').text(semester_name);
        var dates = $(this).closest('.large_semester_square').find('.s_s_dates').text();
        var start_date = dates.substring(0, dates.indexOf(' to ')).trim();
        var end_date = dates.substring(dates.indexOf(' to ') + 4).trim();
        change_dates_start_date_button.val(start_date);
        change_dates_start_date_button.datepicker('option', 'buttonText', start_date);
        change_dates_end_date_button.val(end_date);
        change_dates_end_date_button.datepicker('option', 'buttonText', end_date);
        change_dates_dialog.dialog('open');
    });
	change_dates_dialog.dialog({
		autoOpen: false,
		width: 350,
        resizable: false,
		modal: true,
		buttons: {
			'Change Dates': {
                text: 'Save',
                click: function() {
                    var form = $('#change_dates_form');
                    var new_start_date = change_dates_start_date_button.val();
                    var new_end_date = change_dates_end_date_button.val();

                    $.ajax({
                        type:"POST",
                        url: "/gradebook/overview/",
                        contentType: "application/x-www-form-urlencoded",
                        data: {
                            'post_action': 'change_dates',
                            'semester_id': semester_id,
                            'new_start_date': new_start_date,
                            'new_end_date': new_end_date
                        },
                        success: function(data) {
                            change_dates_dialog.dialog('close');
                            reset_change_dates_form();
                            var data_inside = data.substring(data.indexOf('>') + 1, data.lastIndexOf('<'));
                            var small_square = $('#semester_' + semester_id + '.semester_square');
                            small_square.html(data_inside);
                            var big_square = $('#semester_' + semester_id + '.large_semester_square');
                            big_square.html(data_inside);
                            big_square.find('.hidden_in_s_s_inline').css('display', 'inline-block');
                            big_square.find('.hidden_in_s_s_block').css('display', 'block');
                            big_square.find('.hidden_in_s_s_table_row').css('display', 'table-row');
                            big_square.find('.hidden_in_s_s_table_cell').css('display', 'table-cell');
                            resize_course_table_columns();
                        }
                    });
                }
	      	},
		  	Cancel: function() {
	  			change_dates_dialog.dialog('close');
		  	}
        },
        close: function() {
            reset_change_dates_form();
        }
	});
    function reset_change_dates_form() {
        change_dates_start_date_button.val(getDateFormatted());
        change_dates_start_date_button.datepicker('option', 'buttonText', getDateFormatted());
        change_dates_start_date_button.datepicker('option', 'minDate', '-6Y');
        change_dates_start_date_button.datepicker('option', 'maxDate', '+6Y');
        change_dates_end_date_button.val(getDateFormatted());
        change_dates_end_date_button.datepicker('option', 'buttonText', getDateFormatted());
        change_dates_end_date_button.datepicker('option', 'minDate', '-6Y');
        change_dates_end_date_button.datepicker('option', 'maxDate', '+6Y');
    }
});