$(document).ready(function() {
    var categories_wrapper = $('#categories_wrapper');
    var categories_assignments_wrapper = $('#categories_assignments_wrapper')
    ////////////////////// adding categories //////////////////////
    var add_category_dialog = $('#add_category_dialog_box');
    var add_category_form = $('#add_category_form');
    var add_category_form_is_validated = false;
    add_category_form.jqxValidator({
        focus: false,
        rules: [
            { input: '#add_category_form #name_input', message: 'Name is required', action: 'keyup, blur', rule: 'required' },
            { input: '#add_category_form #worth_input', message: 'Worth is required', action: 'keyup, blur', rule: 'required' },
            { input: '#add_category_form #worth_input', message: 'Worth must be a number', action: 'keyup', rule: 'number' },
            {
                input: '#add_category_form #worth_input', message: 'Worth must be between 0 and 100',
                    action: 'keyup', rule: function (input) {
                        input = parseFloat(input.val());
                        return input >= 0  && input <= 100;
                    }
            },
            {
                input: '#add_category_form #worth_input', message: 'Worth is too large',
                    action: 'keyup', rule: function (input) {
                        if (input.val() === '')
                            return false;
                        var result = false;
                        var backslash_index = window.location.href.lastIndexOf('/', window.location.href.length-2);
                        var id = window.location.href.substring(backslash_index + 1, window.location.href.length-1);
                        $.ajax({
                            type:'GET',
                            async: false,
                            url: '/gradebook/course_detail/' + id + '/',
                            contentType: 'application/x-www-form-urlencoded',
                            data: {
                                'get_action': 'add_category_size_check',
                                'worth': input.val()
                            },
                            success: function(data) {
                                result = data.is_valid;
                            }
                        });
                        return result;
                    }
            }
        ],
        onError: function() {add_category_form_is_validated = false;},
        onSuccess: function() {add_category_form_is_validated = true;}
    });
    categories_assignments_wrapper.on('click', '#add_category_button', function() {
        add_category_dialog.dialog('open');
    });
	add_category_dialog.dialog({
		autoOpen: false,
		width: 350,
        resizable: false,
		modal: true,
		buttons: {
			'Add Category': {
                text: 'Add',
                click: function() {
                    add_category_form.jqxValidator('validate');
                    if (!add_category_form_is_validated)
                        return;
                    var category_name = add_category_form.find('#name_input').val();
                    var category_worth = add_category_form.find('#worth_input').val();
                    var backslash_index = window.location.href.lastIndexOf('/', window.location.href.length-2);
                    var id = window.location.href.substring(backslash_index + 1, window.location.href.length-1);
                    $.ajax({
                        type:'POST',
                        url: '/gradebook/course_detail/' + id + '/',
                        contentType: 'application/x-www-form-urlencoded',
                        data: {
                            'post_action': 'add_category',
                            'category_name': category_name,
                            'category_worth': category_worth
                        },
                        success: function(data) {
                            add_category_dialog.dialog('close');
                            clear_add_category_form_contents();
                            var data_inside = data.substring(data.indexOf('>') + 1, data.lastIndexOf('<'));
                            categories_wrapper.html(data_inside);

                            $.ajax({
                                type:'GET',
                                async: false,
                                url: '/gradebook/course_detail/' + id + '/',
                                contentType: 'application/x-www-form-urlencoded',
                                data: {
                                    'get_action': 'get_category_tree'
                                },
                                success: function(data) {
                                    var data_inside = data.substring(data.indexOf('>') + 1, data.lastIndexOf('<'));
                                    $('#add_category_tree').html(data_inside);
                                    $('#edit_category_tree').html(data_inside);
                                }
                            });
                        }
                    });
                }
	      	},
		  	Cancel: function() {
	  			add_category_dialog.dialog('close');
		  	}
        },
        close: function() {
            clear_add_category_form_contents();
            add_category_form.jqxValidator('hide');
        }
	});
    function clear_add_category_form_contents() {
        add_category_form.find('#name_input').val('');
        add_category_form.find('#worth_input').val('');
    }
    ////////////////////// editing categories //////////////////////
    var edit_category_dialog = $('#edit_category_dialog_box');
    var edit_category_form = $('#edit_category_form');
    var edit_category_form_is_validated = false;
    edit_category_form.jqxValidator({
        focus: false,
        rules: [
            { input: '#edit_category_form #name_input', message: 'Name is required', action: 'keyup, blur', rule: 'required' },
            { input: '#edit_category_form #worth_input', message: 'Worth is required', action: 'keyup, blur', rule: 'required' },
            { input: '#edit_category_form #worth_input', message: 'Worth must be a number', action: 'keyup', rule: 'number' },
            {
                input: '#edit_category_form #worth_input', message: 'Worth must be between 0 and 100',
                    action: 'keyup', rule: function (input) {
                        input = parseFloat(input.val());
                        return input >= 0  && input <= 100;
                    }
            },
            {
                input: '#edit_category_form #worth_input', message: 'Worth is too large',
                    action: 'keyup', rule: function (input) {
                        if (input.val() === '')
                            return false;
                        var result = false;
                        var backslash_index = window.location.href.lastIndexOf('/', window.location.href.length-2);
                        var id = window.location.href.substring(backslash_index + 1, window.location.href.length-1);
                        $.ajax({
                            type:'GET',
                            async: false,
                            url: '/gradebook/course_detail/' + id + '/',
                            contentType: 'application/x-www-form-urlencoded',
                            data: {
                                'get_action': 'edit_category_size_check',
                                'original_worth': original_category_worth,
                                'new_worth': input.val()
                            },
                            success: function(data) {
                                result = data.is_valid;
                            }
                        });
                        return result;
                    }
            }
        ],
        onError: function() {edit_category_form_is_validated = false;},
        onSuccess: function() {edit_category_form_is_validated = true;}
    });
    var category_id;
    var original_category_worth;
    categories_assignments_wrapper.on('click', '#edit_category_button', function() {
        var categories_table_row = $(this).closest('.categories_table_row');
        category_id = categories_table_row.attr('id').split('_').pop();
        edit_category_form.find('#name_input').val(categories_table_row.find('#category_name').text().split(' ')[0]);
        original_category_worth = categories_table_row.find('#category_worth').text().split(' ')[0];
        edit_category_form.find('#worth_input').val(original_category_worth);
        edit_category_dialog.dialog('open');
    });
	edit_category_dialog.dialog({
		autoOpen: false,
		width: 350,
        resizable: false,
		modal: true,
		buttons: {
			'Edit Category': {
                text: 'Save',
                click: function() {
                    edit_category_form.jqxValidator('validate');
                    if (!edit_category_form_is_validated)
                        return;
                    var category_name = edit_category_form.find('#name_input').val();
                    var category_worth = edit_category_form.find('#worth_input').val();
                    var backslash_index = window.location.href.lastIndexOf('/', window.location.href.length-2);
                    var id = window.location.href.substring(backslash_index + 1, window.location.href.length-1);
                    $.ajax({
                        type:'POST',
                        url: '/gradebook/course_detail/' + id + '/',
                        contentType: 'application/x-www-form-urlencoded',
                        data: {
                            'post_action': 'edit_category',
                            'category_id': category_id,
                            'category_name': category_name,
                            'category_worth': category_worth
                        },
                        success: function(data) {
                            edit_category_dialog.dialog('close');
                            var data_inside = data.substring(data.indexOf('>') + 1, data.lastIndexOf('<'));
                            categories_assignments_wrapper.html(data_inside);

                            $.ajax({
                                type:'GET',
                                async: false,
                                url: '/gradebook/course_detail/' + id + '/',
                                contentType: 'application/x-www-form-urlencoded',
                                data: {
                                    'get_action': 'get_category_tree'
                                },
                                success: function(data) {
                                    var add_category_input = $('#add_category_input');
                                    var add_category_tree = add_category_input.find('#category_tree');
                                    console.log(add_category_tree);
                                    add_category_tree.replaceWith(data);
                                    console.log(add_category_tree);
                                    add_category_tree = add_category_input.find('#category_tree');
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
                                    var edit_category_input = $('#edit_category_input');
                                    var edit_category_tree = edit_category_input.find('#category_tree');
                                    edit_category_tree.replaceWith(data);
                                    edit_category_tree = edit_category_input.find('#category_tree');
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
                                }
                            });
                        }
                    });
                }
	      	},
		  	Cancel: function() {
	  			edit_category_dialog.dialog('close');
		  	}
        },
        close: function() {
            edit_category_form.jqxValidator('hide');
        }
	});
    ////////////////////// deleting categories //////////////////////
    var delete_category_dialog = $('#delete_category_dialog_box');
    categories_assignments_wrapper.on('click', '#delete_category_button', function() {
        var categories_table_row = $(this).closest('.categories_table_row');
        category_id = categories_table_row.attr('id').split('_').pop();
        delete_category_dialog.dialog('open');
    });
	delete_category_dialog.dialog({
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
                            'post_action': 'delete_category',
                            'category_id': category_id
                        },
                        success: function(data) {
                            delete_category_dialog.dialog('close');
                            var data_inside = data.substring(data.indexOf('>') + 1, data.lastIndexOf('<'));
                            categories_assignments_wrapper.html(data_inside);
                        }
                    });
                }
	      	},
		  	Cancel: function() {
	  			delete_category_dialog.dialog('close');
		  	}
        },
        close: function() {}
	});
});