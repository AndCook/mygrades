$(document).ready(function() {
    ////////////////////// adding categories //////////////////////
    var add_category_dialog = $('#add_category_dialog_box');
    var add_category_form = $('#add_category_form');
    var add_category_is_validated = false;
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
                            if (input.val() == '')
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
                                    'get_action': 'category_size_check',
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
            onError: function() {add_category_is_validated = false;},
            onSuccess: function() {add_category_is_validated = true;}
        });

    $('#categories_wrapper').on('click', '#add_category_button', function() {
        add_category_dialog.dialog('open');
    });
	add_category_dialog.dialog({
		autoOpen: false,
		width: 350,
        resizable: false,
		modal: true,
		buttons: {
			'Add Category': {
                text: 'Add Category',
                click: function() {
                    add_category_form.jqxValidator('validate');
                    if (!add_category_is_validated)
                        return;
                    var form = $('#add_category_form');
                    var category_name = form.find('#name_input').val();
                    var category_worth = form.find('#worth_input').val();
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
                            clear_category_form_contents();
                            var data_inside = data.substring(data.indexOf('>') + 1, data.lastIndexOf('<'));
                            var category_wrapper = $('#categories_wrapper');
                            category_wrapper.html(data_inside);
                        }
                    });
                }
	      	},
		  	Cancel: function() {
	  			add_category_dialog.dialog('close');
                clear_category_form_contents();
                add_category_form.jqxValidator('hide');
		  	}
        },
        close: function() {
            clear_category_form_contents();
        }
	});
    function clear_category_form_contents() {
        var form = $('#add_category_form');
        form.find('#name_input').val('');
        form.find('#worth_input').val('');
    }
    ////////////////////// editing categories //////////////////////

    ////////////////////// deleting categories //////////////////////
});