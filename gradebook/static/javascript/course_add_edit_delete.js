$(document).ready(function() {
    var semwrap = $('#semester_squares_wrapper');
    var semester_id;
    ////////////////////// adding courses //////////////////////
    var add_course_dialog = $('#add_course_dialog_box');
    var add_course_name = $('#add_course_name');
    var add_course_number = $('#add_course_number');
    var add_course_instructor = $('#add_course_instructor');
    var add_course_hours = $('#add_course_hours');
    add_course_hours.jqxDropDownList({ source: [7,6,5,4,3,2,1,0], selectedIndex: 4, width: '50', height: '25'});
    var add_course_form = $('#add_course_form');
    var add_course_form_is_validated = false;
    add_course_form.jqxValidator({
        focus: false,
        rules: [
            { input: add_course_name, message: 'Name is required', action: 'keyup, blur', rule: 'required' }
        ],
        onError: function() {add_course_form_is_validated = false;},
        onSuccess: function() {add_course_form_is_validated = true;}
    });
    semwrap.on('click', '.add_course', function() {
        semester_id = $(this).closest('.large_semester_square').attr('id').split("_").pop();
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
                    add_course_form.jqxValidator('validate');
                    if (!add_course_form_is_validated)
                        return;

                    var course_name = add_course_name.val();
                    var course_number = add_course_number.val();
                    var course_instructor = add_course_instructor.val();
                    var course_hours = add_course_hours.val();

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
		  	}
        },
        close: function() {
            // clear course form contents
            add_course_name.val('');
            add_course_number.val('');
            add_course_instructor.val('');
            add_course_hours.val(3);
            // clear any visible validators
            add_course_form.jqxValidator('hide');
        }
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
    ////////////////////// editing courses //////////////////////
    var edit_course_dialog = $('#edit_course_dialog_box');
    var edit_course_name = $('#edit_course_name');
    var edit_course_number = $('#edit_course_number');
    var edit_course_instructor = $('#edit_course_instructor');
    var edit_course_hours = $('#edit_course_hours');
    edit_course_hours.jqxDropDownList({ source: [7,6,5,4,3,2,1,0], selectedIndex: 4, width: '50', height: '25'});
    var edit_course_form = $('#edit_course_form');
    var edit_course_form_is_validated = false;
    edit_course_form.jqxValidator({
        focus: false,
        rules: [
            { input: edit_course_name, message: 'Name is required', action: 'keyup, blur', rule: 'required' }
        ],
        onError: function() {edit_course_form_is_validated = false;},
        onSuccess: function() {edit_course_form_is_validated = true;}
    });
    var course_id = -1;
    semwrap.on('click', '.course_edit', function() {
        semester_id = $(this).closest('.large_semester_square').attr('id').split("_").pop();

        var course_tr = $(this).closest('.course_table_row');
        course_id = course_tr.attr('id').split('_').pop();
        var course_name = course_tr.find('.course_name').text().trim();
        var course_number = course_tr.find('.course_number').text().trim();
        var course_instructor = course_tr.find('.course_instructor').text().trim();
        var course_hours = course_tr.find('.course_hours').text().trim().substr(0,1);

        edit_course_name.val(course_name);
        edit_course_number.val(course_number);
        edit_course_instructor.val(course_instructor);
        edit_course_hours.val(course_hours);

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
                    edit_course_form.jqxValidator('validate');
                    if (!edit_course_form_is_validated)
                        return;

                    var course_name = edit_course_name.val();
                    var course_number = edit_course_number.val();
                    var course_instructor = edit_course_instructor.val();
                    var course_hours = edit_course_hours.val();

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
		  	}
        },
        close: function() {/* No need to clear course form contents because they are filled when dialog opens */ }
	});
    ////////////////////// deleting courses //////////////////////
    var delete_course_dialog = $('#delete_course_dialog_box');
    semwrap.on('click', '.course_delete', function() {
        semester_id = $(this).closest('.large_semester_square').attr('id').split("_").pop();
        var course_tr = $(this).closest('.course_table_row');
        course_id = course_tr.attr('id').split('_').pop();
        var course_name = course_tr.find('.course_name').text().trim();
        delete_course_dialog.find('#course_name').text(course_name);
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