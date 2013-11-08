// login dialog box
$(function() {
	var tips = $( ".validate-tips" );

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
	var tips = $( ".validate-tips" );

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

$(function() {
    var accBut = $('#account-button')
    var dropdown = $('#account-dropdown')
    var posLeft = accBut.offset().left + accBut.width() + 20 - dropdown.width();
    var posTop = accBut.offset().top + accBut.height();
    dropdown.css('left', posLeft)
    dropdown.css('top', posTop)

    accBut.mouseenter(function() {
        dropdown.css('display', 'block');
    });

    accBut.mouseleave(function() {
        dropdown.css('display', 'none');
    });

    dropdown.mouseenter(function() {
        dropdown.css('display', 'block');
    })

    dropdown.mouseleave(function() {
        dropdown.css('display', 'none');
    })
});

// enable tooltips everywhere
// to use a tooltip include a title tag on inputs
$(function() {
    $( document ).tooltip();
});