$(function() {
    var semwrap = $('#semester_squares_wrapper');
    var locked = false;
    ////////////////////// expanding a square //////////////////////
    semwrap.on('click', '.semester_square', function() {
        //console.log('expand');
        if (locked)
            return;
        locked = true;
        var big_square = $(this).clone();

        big_square.css('top', $(this).position().top - window.scrollY + 10); // 10 is for margin
        big_square.css('left', $(this).position().left - window.scrollX + 10);
        big_square.css('width', $(this).width());
        big_square.css('height', $(this).height());
        big_square.addClass('large_semester_square');
        big_square.removeClass('semester_square');

        $(this).after(big_square);

        big_square.animate({
            width: '65%',
            height: '65%',
            left: '17.5%',
            top: '17.5%'
        }, 200, function() {
            locked = false;
        });
        var over = $('#overlay');
        over.css('height', $('#middle-section').height());
        over.css('display', 'block');
        over.animate({
            opacity: '0.3'
        }, 200);

        big_square.css('font-size', '1.3em');
        big_square.find('.hidden_in_s_s').css('display', 'inline-block');
    });
    ////////////////////// deleting semesters //////////////////////
    var delete_semester_dialog = $('#delete_semester_dialog_box');
    semwrap.on('click', '.s_s_delete', function() {
        delete_semester_dialog.dialog('open');
    });
    delete_semester_dialog.dialog({
		autoOpen: false,
		width: 350,
        resizable: false,
		modal: true,
		buttons: {
			'Delete Semester': {
                text: 'Delete Semester',
                click: function() {
                    var semester_id = $('.large_semester_square').attr('id');

                    $.ajax({
                        type:"POST",
                        url: "/gradebook/overview/",
                        contentType: "application/x-www-form-urlencoded",
                        data: {
                            'post_action': 'delete_semester',
                            'delete_semester_id': semester_id.split("_").pop()
                        },
                        success: function() {
                            delete_semester_dialog.dialog('close');
                            $('#' + semester_id).remove();
                            $('#overlay').click();
                        }
                    });
                }
	      	},
		  	Cancel: function() {
	  			delete_semester_dialog.dialog('close');
		  	}
        },
        close: function() {}
	});
    ////////////////////// renaming semesters //////////////////////
    var rename_semester_dialog = $('#rename_semester_dialog_box');
    semwrap.on('click', '.s_s_rename', function() {
        rename_semester_dialog.dialog('open');
    });
	rename_semester_dialog.dialog({
		autoOpen: false,
		width: 350,
        resizable: false,
		modal: true,
		buttons: {
			'Rename Semester': {
                text: 'Rename Semester',
                click: function() {
                    var form = $('#rename_semester_form');
                    var new_name = form.find('#id_name').val();

                    if (new_name === '') {
                        var val = form.find('.validation_tips');
                        val.css('display', 'block');
                        val.text('Semester name is required - try again');
                        return;
                    }

                    var semester_id = $('.large_semester_square').attr('id');

                    $.ajax({
                        type:"POST",
                        url: "/gradebook/overview/",
                        contentType: "application/x-www-form-urlencoded",
                        data: {
                            'post_action': 'rename_semester',
                            'rename_semester_id': semester_id.split("_").pop(),
                            'new_semester_name': new_name
                        },
                        success: function() {
                            rename_semester_dialog.dialog('close');
                            clear_semester_form_contents();
                            $('#' + semester_id).find('.s_s_name').text(new_name);
                            $('.large_semester_square').find('.s_s_name').text(new_name);
                        }
                    });
                }
	      	},
		  	Cancel: function() {
	  			rename_semester_dialog.dialog('close');
                clear_semester_form_contents();
		  	}
        },
        close: function() {
            clear_semester_form_contents();
        }
	});
    ////////////////////// shrinking large square //////////////////////
    $('#overlay').click( function() {
        if (locked)
            return;
        locked = true;
        var large_square = $('.large_semester_square');
        large_square.animate({
            opacity: '0'
        }, 200, function() {
            large_square.remove();
            locked = false;
        });
        var over = $('#overlay');
        over.animate({
            opacity: '0'
        }, 200, function() {
            over.css('display', 'none');
        });
    });
    ////////////////////// adding semesters //////////////////////
    var add_semester_dialog = $('#add_semester_dialog_box');
    $('#add_semester_button').click(function() {
        add_semester_dialog.dialog('open');
    });
	add_semester_dialog.dialog({
		autoOpen: false,
		width: 350,
        resizable: false,
		modal: true,
		buttons: {
			'Add Semester': {
                text: 'Add Semester',
                click: function() {
                    var form = $('#add_semester_form');
                    var semester_name = form.find('#id_name').val();

                    if (semester_name === '') {
                        var val = form.find('.validation_tips');
                        val.css('display', 'block');
                        val.text('Semester name is required - try again');
                        return;
                    }

                    $.ajax({
                        type:"POST",
                        url: "/gradebook/overview/",
                        contentType: "application/x-www-form-urlencoded",
                        data: {
                            'post_action': 'add_semester',
                            'semester_name': semester_name
                        },
                        success: function(data) {
                            add_semester_dialog.dialog('close');
                            clear_semester_form_contents();
                            $('#add_semester_button').before(
                                "<div class='semester_square' id='semester_" + data.id + "'>" +
                                "    <div class='s_s_name_div'>" +
                                "       <p class='s_s_name'>" + semester_name + "</p>" +
                                "       <div class='hidden_in_s_s'>" +
                                "           <p class='mini_link s_s_rename'>rename</p>" +
                                "           <p class='mini_link s_s_delete'>delete</p>" +
                                "       </div>" +
                                "    </div>" +
                                "    <table class='semester_square_course_table'><tbody>" +
                                "        <tr class='hidden_in_s_s add_course_tr'>" +
                                "            <td colspan='3'><p class='mini_link add_course'>+ add course</p></td>" +
                                "        </tr>" +
                                "    </tbody></table>" +
                                "</div>"
                            );
                        }
                    });
                }
	      	},
		  	Cancel: function() {
	  			add_semester_dialog.dialog('close');
                clear_semester_form_contents();
		  	}
        },
        close: function() {
            clear_semester_form_contents();
        }
	});
    function clear_semester_form_contents() {
        var form = $('#add_semester_form');
        form.find('#id_name').val('');
    }
    ////////////////////// adding courses //////////////////////
    var add_course_dialog = $('#add_course_dialog_box');
    semwrap.on('click', '.add_course', function() {
        //console.log('add course');
        add_course_dialog.dialog('open');
    });
	add_course_dialog.dialog({
		autoOpen: false,
		width: 350,
        resizable: false,
		modal: true,
		buttons: {
			'Add Course': {
                text: 'Add Course',
                click: function() {
                    var form = $('#add_course_form');
                    var course_name = form.find('#id_name').val();
                    var course_number = form.find('#id_number').val();
                    var course_instructor = form.find('#id_instructor').val();

                    if (course_name === '') {
                        var val = form.find('.validation_tips');
                        val.css('display', 'block');
                        val.text('Course name is required - try again');
                        return;
                    }

                    if (course_number === '')
                        course_number = ' ';
                    if (course_instructor === '')
                        course_instructor = ' ';

                    var semester_id = $('.large_semester_square').attr('id');

                    $.ajax({
                        type:"POST",
                        url: "/gradebook/overview/",
                        contentType: "application/x-www-form-urlencoded",
                        data: {
                            'post_action': 'add_course',
                            'course_name': course_name,
                            'course_number': course_number,
                            'course_instructor': course_instructor,
                            'semester_id': semester_id.split("_").pop()
                        },
                        success: function() {
                            add_course_dialog.dialog('close');
                            clear_course_form_contents();
                            $('#' + semester_id).find('.add_course_tr').before(
                                "<tr>" +
                                "    <td class='s_s_table_data course_number'>" + course_number + "</td>" +
                                "    <td class='s_s_table_data course_name'>" + course_name + "</td>" +
                                "    <td class='s_s_table_data course_grade'>" + "100.0%" + "</td>" +
                                "</tr>"
                            );
                            $('.large_semester_square').find('.add_course_tr').before(
                                "<tr>" +
                                "    <td class='s_s_table_data course_number'>" + course_number + "</td>" +
                                "    <td class='s_s_table_data course_name'>" + course_name + "</td>" +
                                "    <td class='s_s_table_data course_grade'>" + "100.0%" + "</td>" +
                                "</tr>"
                            );
                        }
                    });
                }
	      	},
		  	Cancel: function() {
	  			add_course_dialog.dialog('close');
                clear_course_form_contents();
		  	}
        },
        close: function() {
            clear_course_form_contents();
        }
	});
    function clear_course_form_contents() {
        var form = $('#add_course_form');
        form.find('#id_name').val('');
        form.find('#id_number').val('');
        form.find('#id_instructor').val('');
    }
});
