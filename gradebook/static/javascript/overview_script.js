$(function() {
    var semwrap = $('#semester_squares_wrapper');
    var locked = false;
    ////////////////////// expanding a square //////////////////////
    semwrap.on('click', '.semester_square', function() {
        //console.log('expand');
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

        $(this).after(big_square);

        big_square.animate({
            width: '65%',
            height: '65%',
            left: '17.5%',
            top: '17.5%'
        }, 200, function() {
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
    });
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
        dateFormat: 'M. d, yy',
        numberOfMonths: 2,
        minDate: '-6Y',
        maxDate: '+6Y',
        showOn: 'button',
        buttonText: getDateFormatted(),
        showAnim: 'slideDown',
        // You can put more options here.
        onClose: function( selectedDate ) {
            if (selectedDate !== '')
                add_semester_start_date_button.datepicker('option', 'buttonText', selectedDate);
            add_semester_end_date_button.datepicker('option', 'minDate', selectedDate);
        }
    });
    add_semester_end_date_button.datepicker({
        changeMonth: true,
        changeYear: true,
        dateFormat: 'M. d, yy',
        numberOfMonths: 2,
        minDate: '-6Y',
        maxDate: '+6Y',
        showOn: 'button',
        buttonText: getDateFormatted(),
        showAnim: 'slideDown',
        // You can put more options here.
        onClose: function( selectedDate ) {
            if (selectedDate !== '')
                add_semester_end_date_button.datepicker('option', 'buttonText', selectedDate);
            add_semester_start_date_button.datepicker('option', 'maxDate', selectedDate);
        }
    });
    function getDateFormatted() {
        var currentTime = new Date();
        var day = currentTime.getDate();
        var year = currentTime.getFullYear();
        switch (currentTime.getMonth() + 1) {
            case 1: return 'Jan. ' + day + ', ' + year;
            case 2: return 'Feb. ' + day + ', ' + year;
            case 3: return 'Mar. ' + day + ', ' + year;
            case 4: return 'Apr. ' + day + ', ' + year;
            case 5: return 'May. ' + day + ', ' + year;
            case 6: return 'Jun. ' + day + ', ' + year;
            case 7: return 'Jul. ' + day + ', ' + year;
            case 8: return 'Aug. ' + day + ', ' + year;
            case 9: return 'Sep. ' + day + ', ' + year;
            case 10: return 'Oct. ' + day + ', ' + year;
            case 11: return 'Nov. ' + day + ', ' + year;
            case 12: return 'Dec. ' + day + ', ' + year;
            default: return '';
        }
    }
    var add_semester_dialog = $('#add_semester_dialog_box');
    $('#add_semester_button').click(function() {
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
                            $('#add_semester_button').before(
                                "<div class='semester_square' id='semester_" + data.id + "'>" +
                                "    <div class='s_s_name_div'>" +
                                "       <p class='s_s_name'>" + semester_name + "</p>" +
                                "       <div class='hidden_in_s_s_inline'>" +
                                "           <p class='mini_link s_s_rename'>rename</p>" +
                                "           <p class='mini_link s_s_delete'>delete</p>" +
                                "       </div>" +
                                "    </div>" +

                                "    <div style='text-align: center'>" +
                                "        <p class='hidden_in_s_s_inline s_s_dates' style='margin-right: 5px;'>" +
                                "            " + start_date + " to " + end_date +
                                "        </p>" +
                                "        <p class='hidden_in_s_s_inline mini_link s_s_change_dates'>edit</p>" +
                                "    </div>" +

                                "    <table class='semester_square_course_table'><tbody>" +
                                "        <tr class='hidden_in_s_s_block add_course_tr'>" +
                                "            <td colspan='3'>" +
                                "                <p class='mini_link add_course'>+ add course</p>" +
                                "            </td>" +
                                "        </tr>" +
                                "    </tbody></table>" +
                                "</div>"
                            );
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
        rename_semester_dialog.dialog('open');
    });
	rename_semester_dialog.dialog({
		autoOpen: false,
		width: 350,
        resizable: false,
		modal: true,
		buttons: {
			'Rename Semester': {
                text: 'Rename Semester',
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
                text: 'Delete Semester',
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
        dateFormat: 'M. d, yy',
        numberOfMonths: 2,
        minDate: '-6Y',
        maxDate: '+6Y',
        showOn: 'button',
        buttonText: getDateFormatted(),
        showAnim: 'slideDown',
        // You can put more options here.
        onClose: function( selectedDate ) {
            if (selectedDate !== '')
                change_dates_start_date_button.datepicker('option', 'buttonText', selectedDate);
            change_dates_end_date_button.datepicker('option', 'minDate', selectedDate);
        }
    });
    change_dates_end_date_button.datepicker({
        changeMonth: true,
        changeYear: true,
        dateFormat: 'M. d, yy',
        numberOfMonths: 2,
        minDate: '-6Y',
        maxDate: '+6Y',
        showOn: 'button',
        buttonText: getDateFormatted(),
        showAnim: 'slideDown',
        // You can put more options here.
        onClose: function( selectedDate ) {
            if (selectedDate !== '')
                change_dates_end_date_button.datepicker('option', 'buttonText', selectedDate);
            change_dates_start_date_button.datepicker('option', 'maxDate', selectedDate);
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
                text: 'Change Dates',
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
                        success: function() {
                            change_dates_dialog.dialog('close');
                            reset_change_dates_form();
                            $('#' + semester_id).find('.s_s_dates').text(new_start_date + ' to ' + new_end_date);
                            $('.large_semester_square').find('.s_s_dates').text(new_start_date + ' to ' + new_end_date);
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
        //console.log('add course');
        add_course_dialog.dialog('open');
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
                            'semester_id': semester_id.split("_").pop()
                        },
                        success: function() {
                            add_course_dialog.dialog('close');
                            clear_course_form_contents();
                            $('#' + semester_id).find('.add_course_tr').before(
                                "<tr>" +
                                "    <td class='s_s_table_data course_number'>" + course_number + "</td>" +
                                "    <td class='s_s_table_data course_name'>" + course_name + "</td>" +
                                "    <td class='s_s_table_data course_grade'>" + "100.0%" + "</td>" +
                                "</tr>"
                            );
                            $('.large_semester_square').find('.add_course_tr').before(
                                "<tr>" +
                                "    <td class='s_s_table_data course_number'>" + course_number + "</td>" +
                                "    <td class='s_s_table_data course_name'>" + course_name + "</td>" +
                                "    <td class='s_s_table_data course_grade'>" + "100.0%" + "</td>" +
                                "</tr>"
                            );
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
    ////////////////////// disable coure_link's in semester_square //////////////////////
    semwrap.on('click', '.semester_square .course_link', function(e) {
        e.preventDefault();
    });
});
