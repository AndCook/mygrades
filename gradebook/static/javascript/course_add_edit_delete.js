$(document).ready(function() {
    var semwrap = $('#semester_squares_wrapper');
    var semester_id;
    ////////////////////// adding courses //////////////////////
    var add_course_dialog = $('#add_course_dialog_box');
    semwrap.on('click', '.add_course', function() {
        semester_id = $(this).closest('.large_semester_square').attr('id').split("_").pop();
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
                            'semester_id': semester_id
                        },
                        success: function(data) {
                            add_course_dialog.dialog('close');
                            clear_course_form_contents();
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
    ////////////////////// editing courses //////////////////////
    var edit_course_dialog = $('#edit_course_dialog_box');
    var course_id = -1;
    semwrap.on('click', '.course_edit', function() {
        semester_id = $(this).closest('.large_semester_square').attr('id').split("_").pop();

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
        semester_id = $(this).closest('.large_semester_square').attr('id').split("_").pop();
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
	  			delete_course_dialog.dialog('close');
		  	}
        },
        close: function() {
        }
	});
});