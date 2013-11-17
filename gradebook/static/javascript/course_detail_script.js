// sorting of the data in the assignments table and categories table
$(function(){
    var assignmentsTable = $("#assignments-table")
    var categoriesTable = $("#categories-table")

    assignmentsTable.tablesorter({
        sortReset: true,

        emptyTo: 'bottom',

        // on page load, sort on the sixth column and first column in ascending order
        sortList: [[5,0],[0,0]],

        sortInitialOrder: 'asc',
        headers : {
            2 : { sortInitialOrder: 'desc' }, // awarded points first click is most to least
            3 : { sortInitialOrder: 'desc' }, // possible points first click is most to least
            6: { sorter: false} // don't sort operations column
        }
    });

    assignmentsTable.data("tablesorter").widgets = ["zebra"];
    assignmentsTable.trigger('applyWidgets');

    categoriesTable.tablesorter({
        sortReset: true,

        emptyTo: 'bottom',

        // on page load, sort on the fifth column and first column in ascending order
        sortList: [[4,0],[0,0]],

        sortInitialOrder: 'asc',
        headers : {
            1 : { sortInitialOrder: 'desc' }, // awarded points first click is most to least
            2 : { sortInitialOrder: 'desc' }, // possible points first click is most to least
            5: { sorter: false} // don't sort operations column
        }
    });

    categoriesTable.data("tablesorter").widgets = ["zebra"];
    categoriesTable.trigger('applyWidgets');
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