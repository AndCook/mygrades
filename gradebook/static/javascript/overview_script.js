$(function() {
    // on hover over all semester-square's, change the background-color to #3b3b3b from #222222
    var semester_squares = $('.semester_square');
    var semwrap = $('#semester_squares_wrapper');
    semester_squares.mouseenter(function() {
        $(this).animate({
            backgroundColor: '#3b3b3b'
        }, 100);
    });
    semester_squares.mouseleave(function() {
        $(this).animate({
            backgroundColor: '#222222'
        }, 100);
    });
    var large_semester_squares = $('.large_semester_square');
    semwrap.on('mouseenter', '.large_semester_square', function() {
        $(this).animate({
            backgroundColor: '#306'
        }, 100);
    });
    semwrap.on('mouseleave', '.large_semester_square', function() {
        $(this).animate({
            backgroundColor: '#606'
        }, 100);
    });

    semwrap.on('click', '.semester_square', function() {
        var big_square = $(this).clone();

        big_square.css('position', 'absolute');
        big_square.css('top', $(this).offset().top);
        big_square.css('left', $(this).offset().left);
        big_square.css('width', $(this).width());
        big_square.css('height', $(this).height());
        big_square.css('margin', '0');
        big_square.css('backgroundColor', '#606');
        big_square.css('z-index', '10');
        big_square.addClass('large_semester_square');
        big_square.removeClass('semester_square');

        $(this).after(big_square);

        var leftpos = semester_squares.first().offset().left;

        big_square.animate({
            'width': '71.54%', // 78% width of main wrapper * 98%;
            'left': leftpos
        }, 200);
    });
    semwrap.on('click', '.large_semester_square', function() {
        $(this).animate({
            opacity: '0'
        }, 200, function() {$(this).remove();});
    });

    var add_semester_button = $('#add_semester_button');
    var par = add_semester_button.find('p');
    add_semester_button.mouseenter(function() {
        $(this).animate({
            borderColor: 'red'
        }, 100);
        par.animate({
            color: 'red'
        }, 100);
        $(this).css('background', 'url(/static/images/plus_sign.png) no-repeat center center');
    });
    add_semester_button.mouseleave(function() {
        $(this).animate({
            borderColor: '#3b3b3b'
        }, 100);
        par.animate({
            color: '#3b3b3b'
        }, 100);
        $(this).css('background', 'url(/static/images/plus_sign_light.png) no-repeat center center');
    });

    $('#add_semester_dialog_form').dialog({
		autoOpen: false,
		width: 350,
        resizable: false,
		modal: true,
		buttons: {
			"Add Semester": {
                text: 'Add Semester',
                click: function() {
                    document.forms['add_semester_form'].submit();
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

    add_semester_button.click(function() {
        var name = prompt('Enter Semester Name (ex. "Fall 2014")');

        if (name === null || name === '') {
            alert('Invalid Semester Name');
            return;
        }

        $.ajax({
            type:"POST",
            url: "/gradebook/overview/",
            contentType: "application/x-www-form-urlencoded",
            data: {
                   'new_semester_name': name
            }
        });

        $('#add_semester_button').before(
            "<div class='semester_square'>" +
            "    <p class='semester_square_name'>" + name + "</p>" +
            "</div>"
        );
    });
});

