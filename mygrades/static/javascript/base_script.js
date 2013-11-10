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

// accounts dropdown menu
$(function() {
    var accBut = $('#account-button');
    var dropdown = $('#account-dropdown');
    var posLeft = accBut.offset().left + accBut.width() + 20 - dropdown.width();
    var posTop = accBut.offsetTop + accBut.height();
    dropdown.css('left', posLeft);
    dropdown.css('top', posTop);

    accBut.mouseenter(function() {
        dropdown.slideDown(200);
    });

    accBut.mouseleave(function() {
        dropdown.css('display', 'none');
    });

    dropdown.mouseenter(function() {
        dropdown.css('display', 'block');
    });

    dropdown.mouseleave(function() {
        dropdown.css('display', 'none');
    })
});

$(function() {
    // enable tooltips everywhere
    // to use a tooltip include a title tag on inputs
    $( document ).tooltip();

    // make all submit buttons pretty
    $('input[type=submit]').button();

    // on hover over all header-link's, change the background-color to #333333 from #222222
    var headerlinks = $('.header-link, .dropdown-link');
    headerlinks.mouseenter(function() {
        $(this).animate({
            backgroundColor: '#3b3b3b'
        }, 100);
    });
    headerlinks.mouseleave(function() {
        $(this).animate({
            backgroundColor: '#222222'
        }, 100);
    });
});
