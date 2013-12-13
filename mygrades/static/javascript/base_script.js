$(document).ready(function() {
    // fix width of account button to be the same as the dropdown
    var accBut = $('#account-button');
    var dropdown = $('#account-dropdown');
    if (accBut && dropdown) {
        if (accBut.width() + 20 > dropdown.width())
            dropdown.css('width', accBut.width() + 20);
        else
            accBut.css('width', dropdown.width() - 20);
    }

    // on page load, save default values of all text inputs
    var allTextInputs = $('input[type=text]');
    var defaultValues = {};
    for (var i = 0; i < allTextInputs.size(); i++) {
        var input = allTextInputs.eq(i);
        defaultValues[input.attr('name')] = input.attr('value');
    }

    // the focus and blur event listeners on all text inputs change text color appropriately
    // if text is the original value "First Name", then it is gray, else it is black
    allTextInputs.focus(function() {
        var name = $(this).attr('name');
        if (name in defaultValues) {
            var value = $(this).val();
            var defaultValue = defaultValues[name];
            if (value === defaultValue)
                $(this).val('');
            $(this).css('color', '#222222');
        }
    });

    allTextInputs.blur(function() {
        var name = $(this).attr('name');
        if (name in defaultValues) {
            var value = $(this).val();
            var defaultValue = defaultValues[name];
            if (value === '') {
                $(this).val(defaultValue);
                $(this).css('color', '#999999');
            } else if (value === defaultValue) {
                $(this).css('color', '#999999');
            } else {
                $(this).css('color', '#222222');
            }
        }
    });
});


// login dialog box
$(function() {
	$( "#login-dialog-form" ).dialog({
		autoOpen: false,
		width: 350,
        resizable: false,
		modal: true,
		buttons: {
			'Login': {
                text: 'Login',
                click: function() {
                    document.forms['login_form'].submit();
                }
	      	},
		  	Cancel: function() {
	  			$( this ).dialog( "close" );
		  	}
        },
        close: function() {
            // do special stuff when closing window
            // such as prep for next time window is opened
        }
	});

	$( "#login-button" ).click(function() {
		$( "#login-dialog-form" ).dialog( "open" );
        $('input').blur();
	});
});

// signup dialog box
$(function() {
	$( "#signup-dialog-form" ).dialog({
		autoOpen: false,
		width: 350,
        resizable: false,
		modal: true,
		buttons: {
			"Sign Up": {
                text: 'Sign Up',
                click: function() {
                    document.forms['signup_form'].submit();
                }
	      	},
		  	Cancel: function() {
	  			$( this ).dialog( "close" );
		  	}
        },
        close: function() {
            // do special stuff when closing window
            // such as prep for next time window is opened
        }
    });

	$( "#signup-button" ).click(function() {
		$( "#signup-dialog-form" ).dialog( "open" );
        $('input').blur();
	});
});

// accounts dropdown menu
$(function() {
    var acc = $('#account-button-dropdown');
    if (acc) {
        var dropdown = $('#account-dropdown');

        acc.mouseenter(function() {
            dropdown.slideDown(200);
        });

        acc.mouseleave(function() {
            dropdown.css('display', 'none');
        });
    }
});

$(function() {
    // enable tooltips everywhere
    // to use a tooltip include a title tag on inputs
    $( document ).tooltip();

    // make all submit buttons pretty
    $('input[type=submit]').button();
});

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    crossDomain: false, // obviates need for sameOrigin test
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
            var csrftoken = $.cookie('csrftoken');
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});