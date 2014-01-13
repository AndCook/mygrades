$(function() {
    var semwrap = $('#semester_squares_wrapper');
    var locked = false;
    ////////////////////// expanding a square //////////////////////
    semwrap.on('click', '.semester_square', function() {
        if (locked)
            return;
        locked = true;
        var big_square = $(this).clone();

        big_square.css('top', $(this).position().top - window.scrollY + 10); // 10 is for margin
        big_square.css('left', $(this).position().left - window.scrollX + 10);
        big_square.css('width', $(this).width());
        big_square.css('height', $(this).height());
        big_square.addClass('large_semester_square');
        big_square.removeClass('semester_square');

        var new_width = Math.max(.65*$(window).innerWidth(), 600);
        var new_height = Math.max(.65*$(window).innerHeight(), 450);

        $(this).after(big_square);

        big_square.animate({
            width: new_width,
            height: new_height,
            left: ($(window).innerWidth() - new_width) / 2,
            top: ($(window).innerHeight() - new_height) / 2
        }, 200, function() {
            big_square.css('min-width', '600px');
            big_square.css('min-height', '450px');
            locked = false;
        });
        var over = $('#overlay');
        over.css('height', $('#middle_section').height());
        over.css('display', 'block');
        over.animate({
            opacity: '0.3'
        }, 200);

        big_square.css('font-size', '1.3em');
        big_square.find('.hidden_in_s_s_inline').css('display', 'inline-block');
        big_square.find('.hidden_in_s_s_block').css('display', 'block');
        big_square.find('.hidden_in_s_s_table_row').css('display', 'table-row');
        big_square.find('.hidden_in_s_s_table_cell').css('display', 'table-cell');
        resize_course_table_columns();

        $(window).resize(function () {
            big_square.css('left', ($(window).innerWidth() - big_square.width()) / 2);
            big_square.css('top', ($(window).innerHeight() - big_square.height()) / 2);
        });
    });
    function resize_course_table_columns() {
        var big_square = $('.large_semester_square');
        big_square.find('.course_number').css('width', '13%');
        big_square.find('.course_hours').css('width', '8%');
        big_square.find('.course_name').css('width', '35%');
        big_square.find('.course_instructor').css('width', '25%');
        big_square.find('.course_grade').css('width', '10%');
        big_square.find('.course_edit').css('width', '4%');
        big_square.find('.course_delete').css('width', '5%');
    }
    ////////////////////// shrinking large square //////////////////////
    $('#overlay, #header, #footer').click( function() {
        if (locked)
            return;
        locked = true;
        var large_square = $('.large_semester_square');
        large_square.animate({
            opacity: '0'
        }, 200, function() {
            large_square.remove();
            locked = false;
        });
        var over = $('#overlay');
        over.animate({
            opacity: '0'
        }, 200, function() {
            over.css('display', 'none');
        });
    });
    ////////////////////// adding semesters //////////////////////
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
                    var form = $('#add_semester_form');
                    var semester_name = form.find('#id_name').val();
                    var start_date = add_semester_start_date_button.val();
                    var end_date = add_semester_end_date_button.val();

                    if (semester_name === '') {
                        var val = form.find('.validation_tips');
                        val.css('display', 'block');
                        val.text('Semester name is required - try again');
                        return;
                    }

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
                            reset_add_semester_form();
                            $('#add_semester_button').before(data);
                        }
                    });
                }
	      	},
		  	Cancel: function() {
	  			add_semester_dialog.dialog('close');
                reset_add_semester_form();
		  	}
        },
        close: function() {
            reset_add_semester_form();
        }
	});
    function reset_add_semester_form() {
        $('#add_semester_form').find('#id_name').val('');
        add_semester_start_date_button.val(getDateFormatted());
        add_semester_start_date_button.datepicker('option', 'buttonText', getDateFormatted());
        add_semester_start_date_button.datepicker('option', 'minDate', '-6Y');
        add_semester_start_date_button.datepicker('option', 'maxDate', '+6Y');
        add_semester_end_date_button.val(getDateFormatted());
        add_semester_end_date_button.datepicker('option', 'buttonText', getDateFormatted());
        add_semester_end_date_button.datepicker('option', 'minDate', '-6Y');
        add_semester_end_date_button.datepicker('option', 'maxDate', '+6Y');
    }
    ////////////////////// renaming semesters //////////////////////
    var rename_semester_dialog = $('#rename_semester_dialog_box');
    semwrap.on('click', '.s_s_rename', function() {
        var semester_name = $(this).closest('.s_s_name_div').find('.s_s_name').text().trim();
        rename_semester_dialog.find('#id_name').val(semester_name);
        rename_semester_dialog.find('#id_name').css('color', '#222222');
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
                    var form = $('#rename_semester_form');
                    var new_name = form.find('#id_name').val();

                    if (new_name === '') {
                        var val = form.find('.validation_tips');
                        val.css('display', 'block');
                        val.text('Semester name is required - try again');
                        return;
                    }

                    var semester_id = $('.large_semester_square').attr('id');

                    $.ajax({
                        type:"POST",
                        url: "/gradebook/overview/",
                        contentType: "application/x-www-form-urlencoded",
                        data: {
                            'post_action': 'rename_semester',
                            'semester_id': semester_id.split("_").pop(),
                            'new_semester_name': new_name
                        },
                        success: function() {
                            rename_semester_dialog.dialog('close');
                            $('#rename_semester_form').find('#id_name').val('');
                            $('#' + semester_id).find('.s_s_name').text(new_name);
                            $('.large_semester_square').find('.s_s_name').text(new_name);
                        }
                    });
                }
	      	},
		  	Cancel: function() {
	  			rename_semester_dialog.dialog('close');
                $('#rename_semester_form').find('#id_name').val('');
		  	}
        },
        close: function() {
            $('#rename_semester_form').find('#id_name').val('');
        }
	});
    ////////////////////// deleting semesters //////////////////////
    var delete_semester_dialog = $('#delete_semester_dialog_box');
    semwrap.on('click', '.s_s_delete', function() {
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
                    var semester_id = $('.large_semester_square').attr('id');

                    $.ajax({
                        type:"POST",
                        url: "/gradebook/overview/",
                        contentType: "application/x-www-form-urlencoded",
                        data: {
                            'post_action': 'delete_semester',
                            'semester_id': semester_id.split("_").pop()
                        },
                        success: function() {
                            delete_semester_dialog.dialog('close');
                            $('#' + semester_id).remove();
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
        var dates = $('.large_semester_square').find('.s_s_dates').text();
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

                    var semester_id = $('.large_semester_square').attr('id');

                    $.ajax({
                        type:"POST",
                        url: "/gradebook/overview/",
                        contentType: "application/x-www-form-urlencoded",
                        data: {
                            'post_action': 'change_dates',
                            'semester_id': semester_id.split("_").pop(),
                            'new_start_date': new_start_date,
                            'new_end_date': new_end_date
                        },
                        success: function(data) {
                            change_dates_dialog.dialog('close');
                            reset_change_dates_form();
                            $('#' + semester_id).replaceWith(data);
                            var big_square = $('.large_semester_square');
                            // must use duplicate jquery selectors here - ignore error
                            big_square.html($('#' + semester_id).html());
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
                reset_change_dates_form();
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
    ////////////////////// adding courses //////////////////////
    var add_course_dialog = $('#add_course_dialog_box');
    semwrap.on('click', '.add_course', function() {
        add_course_dialog.dialog('open');
        $('#id_hours').val(3);
    });
	add_course_dialog.dialog({
		autoOpen: false,
		width: 350,
        resizable: false,
		modal: true,
		buttons: {
			'Add Course': {
                text: 'Add Course',
                click: function() {
                    var form = $('#add_course_form');
                    var course_name = form.find('#id_name').val();
                    var course_number = form.find('#id_number').val();
                    var course_instructor = form.find('#id_instructor').val();
                    var course_hours = form.find('#id_hours').val();

                    if (course_name === '') {
                        var val = form.find('.validation_tips');
                        val.css('display', 'block');
                        val.text('Course name is required - try again');
                        return;
                    }

                    if (course_number === '')
                        course_number = ' ';
                    if (course_instructor === '')
                        course_instructor = ' ';

                    var semester_id = $('.large_semester_square').attr('id');

                    $.ajax({
                        type:"POST",
                        url: "/gradebook/overview/",
                        contentType: "application/x-www-form-urlencoded",
                        data: {
                            'post_action': 'add_course',
                            'course_name': course_name,
                            'course_number': course_number,
                            'course_instructor': course_instructor,
                            'course_hours': course_hours,
                            'semester_id': semester_id.split("_").pop()
                        },
                        success: function(data) {
                            add_course_dialog.dialog('close');
                            clear_course_form_contents();
                            $('#' + semester_id).replaceWith(data);
                            var big_square = $('.large_semester_square');
                            // must use duplicate jquery selectors here - ignore error
                            big_square.html($('#' + semester_id).html());
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
	  			add_course_dialog.dialog('close');
                clear_course_form_contents();
		  	}
        },
        close: function() {
            clear_course_form_contents();
        }
	});
    function clear_course_form_contents() {
        var form = $('#add_course_form');
        form.find('#id_name').val('');
        form.find('#id_number').val('');
        form.find('#id_instructor').val('');
    }
    ////////////////////// editing courses //////////////////////
    var edit_course_dialog = $('#edit_course_dialog_box');
    var course_id = -1;
    semwrap.on('click', '.course_edit', function() {
        var course_tr = $(this).closest('.course_table_row');
        course_id = course_tr.attr('id').split('_').pop();
        var course_name = course_tr.find('.course_name').text().trim();
        var course_number = course_tr.find('.course_number').text().trim();
        var course_instructor = course_tr.find('.course_instructor').text().trim();
        var course_hours = course_tr.find('.course_hours').text().trim().substr(0,1);

        edit_course_dialog.find('#id_name').val(course_name);
        edit_course_dialog.find('#id_number').val(course_number);
        edit_course_dialog.find('#id_instructor').val(course_instructor);
        edit_course_dialog.find('#id_hours').val(course_hours);

        edit_course_dialog.find('#id_name').css('color', '#222222');
        edit_course_dialog.find('#id_number').css('color', '#222222');
        edit_course_dialog.find('#id_instructor').css('color', '#222222');

        edit_course_dialog.find('a').attr('href', '/gradebook/course_detail/' + course_id + '/');

        edit_course_dialog.dialog('open');
    });
	edit_course_dialog.dialog({
		autoOpen: false,
		width: 350,
        resizable: false,
		modal: true,
		buttons: {
			'Edit Course': {
                text: 'Save',
                click: function() {
                    var form = $('#edit_course_form');
                    var course_name = form.find('#id_name').val();
                    var course_number = form.find('#id_number').val();
                    var course_instructor = form.find('#id_instructor').val();
                    var course_hours = form.find('#id_hours').val();

                    if (course_name === '') {
                        var val = form.find('.validation_tips');
                        val.css('display', 'block');
                        val.text('Course name is required - try again');
                        return;
                    }

                    if (course_number === '')
                        course_number = ' ';
                    if (course_instructor === '')
                        course_instructor = ' ';

                    $.ajax({
                        type:"POST",
                        url: "/gradebook/overview/",
                        contentType: "application/x-www-form-urlencoded",
                        data: {
                            'post_action': 'edit_course',
                            'course_id': course_id,
                            'course_name': course_name,
                            'course_number': course_number,
                            'course_instructor': course_instructor,
                            'course_hours': course_hours
                        },
                        success: function(data) {
                            edit_course_dialog.dialog('close');
                            clear_course_form_contents();
                            var semester_id = $('#course_' + course_id).closest('.semester_square').attr('id');
                            $('#' + semester_id).replaceWith(data);
                            var big_square = $('.large_semester_square');
                            // must use duplicate jquery selectors here - ignore error
                            big_square.html($('#' + semester_id).html());
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
	  			edit_course_dialog.dialog('close');
                clear_course_form_contents();
		  	}
        },
        close: function() {
            clear_course_form_contents();
        }
	});
    ////////////////////// deleting courses //////////////////////
    var delete_course_dialog = $('#delete_course_dialog_box');
    semwrap.on('click', '.course_delete', function() {
        var course_tr = $(this).closest('.course_table_row');
        course_id = course_tr.attr('id').split('_').pop();
        delete_course_dialog.dialog('open');
    });
	delete_course_dialog.dialog({
		autoOpen: false,
		width: 350,
        resizable: false,
		modal: true,
		buttons: {
			'Delete Course': {
                text: 'Delete',
                click: function() {

                    $.ajax({
                        type:"POST",
                        url: "/gradebook/overview/",
                        contentType: "application/x-www-form-urlencoded",
                        data: {
                            'post_action': 'delete_course',
                            'course_id': course_id
                        },
                        success: function(data) {
                            delete_course_dialog.dialog('close');
                            var semester_id = $('#course_' + course_id).closest('.semester_square').attr('id');
                            $('#' + semester_id).replaceWith(data);
                            var big_square = $('.large_semester_square');
                            // must use duplicate jquery selectors here - ignore error
                            big_square.html($('#' + semester_id).html());
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
	  			delete_course_dialog.dialog('close');
		  	}
        },
        close: function() {
        }
	});
    ////////////////////// disable coure_link's in semester_square //////////////////////
    semwrap.on('click', '.semester_square .course_link', function(e) {
        e.preventDefault();
    });
});
