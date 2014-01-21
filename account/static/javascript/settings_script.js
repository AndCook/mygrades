$(document).ready(function() {
    var change_form = $('#change_settings_form');
    var submit_button = $('#settings_form_submit_button');
    submit_button.jqxButton();
    submit_button.click(function(e) {
        change_form.jqxValidator('validate');
        if (!settings_is_validated)
            e.preventDefault();
        console.log(settings_is_validated);
    });

    var settings_is_validated = false;

    change_form.jqxValidator({
        focus: false,
        rules: [
            { input: '#change_settings_form #id_email', message: 'Invalid e-mail address', action: 'blur', rule: 'email' },
            {
                input: '#change_settings_form #id_email', message: 'An account is already associated\nwith this email address',
                    action: 'blur', rule: function (input) {
                        var result = false;
                        $.ajax({
                            type:'GET',
                            async: false,
                            url: '/account/settings/',
                            contentType: 'application/x-www-form-urlencoded',
                            data: {
                                'get_action': 'is_email_unique',
                                'email_in_question': input.val().trim()
                            },
                            success: function(data) {
                                result = data.is_unique;
                            }
                        });
                        //console.log(result);
                        return result;
                    }
            },
            { input: '#change_settings_form #id_first_name', message: 'Your first name must contain only letters', action: 'keyup', rule: 'notNumber' },
            { input: '#change_settings_form #id_last_name', message: 'Your last name must contain only letters', action: 'keyup', rule: 'notNumber' }
        ],
        onError: function() {settings_is_validated = false;},
        onSuccess: function() {settings_is_validated = true;}
    });
});