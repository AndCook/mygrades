// login dialog box
$(function() {
	var tips = $( ".validate-tips" );

	$( "#login-dialog-form" ).dialog({
		autoOpen: false,
		height: 400,
		width: 400,
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

	$( "#login-button" ).button().click(function() {
		$( "#login-dialog-form" ).dialog( "open" );
	});
});

// signup dialog box
$(function() {
	var tips = $( ".validate-tips" );

	$( "#signup-dialog-form" ).dialog({
		autoOpen: false,
		height: 400,
		width: 400,
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

	$( "#signup-button" ).button().click(function() {
		$( "#signup-dialog-form" ).dialog( "open" );
	});
});