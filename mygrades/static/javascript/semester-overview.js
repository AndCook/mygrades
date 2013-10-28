// draggable sorting of the course list
$(function() {
    var sort = $('#sortable-courselist');
    sort.sortable({
      	placeholder: 'course placeholder'
    });
    sort.disableSelection();
});

// add course dialog box
$(function() {
	var number = $( "#number" );
	var name = $( "#name" );
	var instructor = $( "#instructor" );
	//var allFields = $( [] ).add( number ).add( name ).add( instructor );
	var tips = $( ".validate-tips" );

	$( "#add-course-dialog-form" ).dialog({
		autoOpen: false,
		height: 325,
		width: 375,
		modal: true,
		buttons: {
			"Add course": function() {
				var isValid = true;

				// do stuff to check for validity of inputs

		        if ( isValid ) {
	      			// store data in database
	      			$( this ).dialog( "close" );
	    	  	} else {
	    	  		// change validate-tips to help user type valid inputs
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

	$( ".add-course-button" ).button().click(function() {
		$( "#add-course-dialog-form" ).dialog( "open" );
	});
});

