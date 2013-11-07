// sorting of both the course list and assignment lists
$(function() {
    var sort = $('#sortable-courselist');
    sort.sortable({
      	placeholder: 'course placeholder'
    });
    sort.disableSelection();

    var sort2 = $('.sortable-assignmentlist');
    sort2.sortable({
      	placeholder: 'assignment placeholder'
    });
    sort2.disableSelection();
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

// add assignment dialog box
$(function() {
	var name = $( "#name" );
	var awardedPoints = $( "#awarded-points" );
	var possiblePoints = $( "#possible-points" );
	//var allFields = $( [] ).add( name ).add( awardedPoints ).add( possiblePoints );
	var tips = $( ".validate-tips" );

	$( "#add-assignment-dialog-form" ).dialog({
		autoOpen: false,
		height: 325,
		width: 375,
		modal: true,
		buttons: {
			"Add assignment": function() {
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

	$( ".add-assignment-button" ).button().click(function() {
		$( "#add-assignment-dialog-form" ).dialog( "open" );
	});
});

// assignment editing
$(function() {

	$( ".edit-button" ).button().click(function() {
		// do stuff
	});
});

// assignment deletion
$(function() {

	$( ".delete-button" ).button().click(function() {
		// do stuff
	});
});