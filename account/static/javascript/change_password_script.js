$(document).ready(function() {
    var submit_button = $('#change_password_submit_button');
    submit_button.jqxButton();
    submit_button.click(function(e) {
            change_password_form.jqxValidator('validate');
            if (!change_password_is_validated)
                e.preventDefault();
        });

    var change_password_is_validated = false;
    var change_password_form = $('#change_password_form');

    change_password_form.jqxValidator({
        focus: false,
        rules: [
            { input: '#change_password_form #id_new_password1', message: 'Password is required', action: 'keyup, blur', rule: 'required' },
            { input: '#change_password_form #id_new_password1', message: 'Your password must be between 8 and 30 characters', action: 'keyup, blur', rule: 'length=8,30' },
            { input: '#change_password_form #id_new_password2', message: 'Password is required', action: 'keyup, blur', rule: 'required' },
            {
                input: '#change_password_form #id_new_password2', message: 'Passwords don\'t match',
                    action: 'keyup, focus', rule: function (input) {
                        // call commit with false, when you are doing server validation
                        // and you want to display a validation error on this field.
                        return input.val() === change_password_form.find('#id_new_password1').val();
                    }
            }
        ],
        onError: function() {change_password_is_validated = false;},
        onSuccess: function() {change_password_is_validated = true;}
    });
});