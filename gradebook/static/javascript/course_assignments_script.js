$(document).ready(function() {
    var categories_assignments_wrapper = $('#categories_assignments_wrapper');
    function xor(bool1, bool2) {
        return (bool1 && !bool2) || (!bool1 && bool2);
    }
    ////////////////////// adding assignments //////////////////////
    var add_assignment_dialog = $('#add_assignment_dialog_box');
    var add_assignment_form = $('#add_assignment_form');
    var add_name_input = add_assignment_form.find('#name_input');
    var add_grade_unknown_button = add_assignment_form.find('#grade_unknown_input');
    var add_points_earned_input = add_assignment_form.find('#points_earned_input');
    var add_total_points_input = add_assignment_form.find('#total_points_input');
    add_grade_unknown_button.jqxCheckBox({ width: 130});
    add_grade_unknown_button.on('checked',
        function () {
            add_points_earned_input.val('');
            add_points_earned_input.prop('disabled', true);
        });
    add_grade_unknown_button.on('unchecked',
        function () {
            add_points_earned_input.prop('disabled', false);
        });
    var add_category_input = $('#add_category_input');
    var add_category_tree = $('#add_category_tree');
    add_category_input.jqxDropDownButton({ width: 185, height: 25 });
    add_category_tree.on('select', function (event) {
        var args = event.args;
        var item = add_category_tree.jqxTree('getItem', args.element);
        if (item !== null) {
            var dropDownContent = '<div style="position: relative; margin-left: 3px; margin-top: 5px;">' + item.label + '</div>';
            add_category_input.jqxDropDownButton('setContent', dropDownContent);
        }
        add_category_input.jqxDropDownButton('close');
    });
    add_category_tree.jqxTree({ width: 185, height: 150 });
    add_category_tree.jqxTree('selectItem', add_category_tree.find('li:first')[0]);
    var add_assignment_form_is_validated = false;
    add_assignment_form.jqxValidator({
        focus: false,
        rules: [
            { input: add_name_input, message: 'Name is required', action: 'keyup', rule: 'required' },
            { input: add_points_earned_input, message: 'Points earned must be a number', action: 'keyup', rule: 'number' },
            {
                input: add_points_earned_input,  message: 'Points earned or grade unknown is required',
                action: 'blur', rule: function (input) {
                    var grade_unknown = add_grade_unknown_button.val();
                    var points_entered = input.val().length > 0;
                    return xor(grade_unknown, points_entered);
                }
            },
            { input: add_total_points_input, message: 'Total points is required', action: 'keyup', rule: 'required' },
            { input: add_total_points_input, message: 'Total points must be a number', action: 'keyup', rule: 'number' },
            {
                input: add_total_points_input, message: 'Total points can\'t be negative',
                action: 'blur', rule: function(input) {
                   return input.val().length === 0 || parseFloat(input.val()) >= 0;
                }
            }
        ],
        onError: function() {add_assignment_form_is_validated = false;},
        onSuccess: function() {add_assignment_form_is_validated = true;}
    });
    categories_assignments_wrapper.on('click', '#add_assignment_button', function() {
        add_assignment_dialog.dialog('open');
    });
	add_assignment_dialog.dialog({
		autoOpen: false,
		width: 350,
        resizable: false,
		modal: true,
		buttons: {
			'Add Assignment': {
                text: 'Add',
                click: function() {
                    add_assignment_form.jqxValidator('validate');
                    if (!add_assignment_form_is_validated)
                        return;
                    var name = add_name_input.val();

                    var val = add_category_tree.jqxTree('getSelectedItem').element.innerHTML;
                    var id_index = val.indexOf('id="category_') + 13;
                    var end_id_index = val.indexOf('">', id_index);
                    var category_id = val.substring(id_index, end_id_index);

                    var grade_unknown = add_grade_unknown_button.val();
                    var points_earned = add_points_earned_input.val();
                    var total_points = add_total_points_input.val();
                    var backslash_index = window.location.href.lastIndexOf('/', window.location.href.length-2);
                    var id = window.location.href.substring(backslash_index + 1, window.location.href.length-1);
                    $.ajax({
                        type:'POST',
                        url: '/gradebook/course_detail/' + id + '/',
                        contentType: 'application/x-www-form-urlencoded',
                        data: {
                            'post_action': 'add_assignment',
                            'assignment_name': name,
                            'assignment_category_id': category_id,
                            'assignment_grade_unknown': grade_unknown,
                            'assignment_points_earned': points_earned,
                            'assignment_total_points': total_points
                        },
                        success: function(data) {
                            add_assignment_dialog.dialog('close');
                            clear_add_assignment_form_contents();
                            var data_inside = data.substring(data.indexOf('>') + 1, data.lastIndexOf('<'));
                            categories_assignments_wrapper.html(data_inside);
                        }
                    });
                }
	      	},
		  	Cancel: function() {
	  			add_assignment_dialog.dialog('close');
		  	}
        },
        close: function() {
            clear_add_assignment_form_contents();
            add_assignment_form.jqxValidator('hide');
        }
	});
    function clear_add_assignment_form_contents() {
        add_name_input.val('');
        add_grade_unknown_button.val(false);
        add_points_earned_input.val('');
        add_total_points_input.val('');
    }
    ////////////////////// editing assignments //////////////////////
    var edit_assignment_dialog = $('#edit_assignment_dialog_box');
    var edit_assignment_form = $('#edit_assignment_form');
    var edit_name_input = edit_assignment_form.find('#name_input');
    var edit_grade_unknown_button = edit_assignment_form.find('#grade_unknown_input');
    var edit_points_earned_input = edit_assignment_form.find('#points_earned_input');
    var edit_total_points_input = edit_assignment_form.find('#total_points_input');
    edit_grade_unknown_button.jqxCheckBox({ width: 130});
    edit_grade_unknown_button.on('checked',
        function () {
            edit_points_earned_input.val('');
            edit_points_earned_input.prop('disabled', true);
        });
    edit_grade_unknown_button.on('unchecked',
        function () {
            edit_points_earned_input.prop('disabled', false);
        });
    var edit_category_input = $('#edit_category_input');
    var edit_category_tree = $('#edit_category_tree');
    edit_category_input.jqxDropDownButton({ width: 185, height: 25 });
    edit_category_tree.on('select', function (event) {
        var args = event.args;
        var item = edit_category_tree.jqxTree('getItem', args.element);
        if (item !== null) {
            var dropDownContent = '<div style="position: relative; margin-left: 3px; margin-top: 5px;">' + item.label + '</div>';
            edit_category_input.jqxDropDownButton('setContent', dropDownContent);
        }
        edit_category_input.jqxDropDownButton('close');
    });
    edit_category_tree.jqxTree({ width: 185, height: 150 });
    edit_category_tree.jqxTree('selectItem', edit_category_tree.find('li:first')[0]);
    var edit_assignment_form_is_validated = false;
    edit_assignment_form.jqxValidator({
        focus: false,
        rules: [
            { input: edit_name_input, message: 'Name is required', action: 'keyup', rule: 'required' },
            { input: edit_points_earned_input, message: 'Points earned must be a number', action: 'keyup', rule: 'number' },
            {
                input: edit_points_earned_input, message: 'Points earned or grade unknown is required',
                action: 'blur', rule: function (input) {
                    var grade_unknown = edit_grade_unknown_button.val();
                    var points_entered = input.val().length > 0;
                    return xor(grade_unknown, points_entered);
                }
            },
            { input: edit_total_points_input, message: 'Total points is required', action: 'keyup', rule: 'required' },
            { input: edit_total_points_input, message: 'Total points must be a number', action: 'keyup', rule: 'number' },
            {
                input: edit_total_points_input, message: 'Total points can\'t be negative',
                action: 'blur', rule: function(input) {
                   return input.val().length === 0 || parseFloat(input.val()) >= 0;
                }
            }
        ],
        onError: function() {edit_assignment_form_is_validated = false;},
        onSuccess: function() {edit_assignment_form_is_validated = true;}
    });
    var assignment_id;
    categories_assignments_wrapper.on('click', '#edit_assignment_button', function() {
        var assignments_table_row = $(this).closest('.assignments_table_row');
        assignment_id = assignments_table_row.attr('id').split('_').pop();
        edit_name_input.val(assignments_table_row.find('#assignment_name').text().trim());

        var current_category = assignments_table_row.find('#assignment_category').text().trim();
        edit_category_tree.jqxTree('selectItem', $('#' + current_category)[0]);

        var assignment_points = assignments_table_row.find('#assignment_points').text().split(' / ');
        var points_earned = assignment_points[0].trim();
        if (points_earned === '?') {
            edit_grade_unknown_button.val(true);
            edit_points_earned_input.val('');
        } else {
            edit_grade_unknown_button.val(false);
            edit_points_earned_input.val(points_earned);
        }
        edit_total_points_input.val(assignment_points[1].trim());
        edit_assignment_dialog.dialog('open');
    });
	edit_assignment_dialog.dialog({
		autoOpen: false,
		width: 350,
        resizable: false,
		modal: true,
		buttons: {
			'Edit Assignment': {
                text: 'Save',
                click: function() {
                    edit_assignment_form.jqxValidator('validate');
                    if (!edit_assignment_form_is_validated)
                        return;
                    var name = edit_name_input.val();

                    var val = edit_category_tree.jqxTree('getSelectedItem').element.innerHTML;
                    var id_index = val.indexOf('id="category_') + 13;
                    var end_id_index = val.indexOf('">', id_index);
                    var category_id = val.substring(id_index, end_id_index);

                    var grade_unknown = edit_grade_unknown_button.val();
                    var points_earned = edit_points_earned_input.val();
                    var total_points = edit_total_points_input.val();
                    var backslash_index = window.location.href.lastIndexOf('/', window.location.href.length-2);
                    var id = window.location.href.substring(backslash_index + 1, window.location.href.length-1);
                    $.ajax({
                        type:'POST',
                        url: '/gradebook/course_detail/' + id + '/',
                        contentType: 'application/x-www-form-urlencoded',
                        data: {
                            'post_action': 'edit_assignment',
                            'assignment_id': assignment_id,
                            'new_category_id': category_id,
                            'new_name': name,
                            'new_grade_unknown': grade_unknown,
                            'new_points_earned': points_earned,
                            'new_total_points': total_points
                        },
                        success: function(data) {
                            edit_assignment_dialog.dialog('close');
                            var data_inside = data.substring(data.indexOf('>') + 1, data.lastIndexOf('<'));
                            categories_assignments_wrapper.html(data_inside);
                        }
                    });
                }
	      	},
		  	Cancel: function() {
	  			edit_assignment_dialog.dialog('close');
		  	}
        },
        close: function() {
            edit_assignment_form.jqxValidator('hide');
        }
	});
    ////////////////////// deleting assignments //////////////////////
    var delete_assignment_dialog = $('#delete_assignment_dialog_box');
    categories_assignments_wrapper.on('click', '#delete_assignment_button', function() {
        var assignments_table_row = $(this).closest('.assignments_table_row');
        assignment_id = assignments_table_row.attr('id').split('_').pop();
        delete_assignment_dialog.dialog('open');
    });
	delete_assignment_dialog.dialog({
		autoOpen: false,
		width: 350,
        resizable: false,
		modal: true,
		buttons: {
			'Delete': {
                text: 'Delete',
                click: function() {
                    var backslash_index = window.location.href.lastIndexOf('/', window.location.href.length-2);
                    var id = window.location.href.substring(backslash_index + 1, window.location.href.length-1);
                    $.ajax({
                        type:'POST',
                        url: '/gradebook/course_detail/' + id + '/',
                        contentType: 'application/x-www-form-urlencoded',
                        data: {
                            'post_action': 'delete_assignment',
                            'assignment_id': assignment_id
                        },
                        success: function(data) {
                            delete_assignment_dialog.dialog('close');
                            var data_inside = data.substring(data.indexOf('>') + 1, data.lastIndexOf('<'));
                            categories_assignments_wrapper.html(data_inside);
                        }
                    });
                }
	      	},
		  	Cancel: function() {
	  			delete_assignment_dialog.dialog('close');
		  	}
        },
        close: function() {}
	});
});