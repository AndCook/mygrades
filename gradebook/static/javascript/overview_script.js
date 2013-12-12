$(function() {
    ////////////////////// semester squares color animation //////////////////////
    var semwrap = $('#semester_squares_wrapper');
    semwrap.on('mouseenter', '.semester_square', function() {
        $(this).animate({
            backgroundColor: '#3b3b3b'
        }, 100);
    });
    semwrap.on('mouseleave', '.semester_square', function() {
        $(this).animate({
            backgroundColor: '#222222'
        }, 100);
    });
    /*semwrap.on('mouseenter', '.large_semester_square', function() {
        $(this).animate({
            backgroundColor: '#3b3b3b'
        }, 100);
    });
    semwrap.on('mouseleave', '.large_semester_square', function() {
        $(this).animate({
            backgroundColor: '#222222'
        }, 100);
    });*/

    var locked = false;
    ////////////////////// expanding a square //////////////////////
    semwrap.on('click', '.semester_square', function() {
        //console.log('expand');
        if (locked)
            return;
        locked = true;
        var big_square = $(this).clone();

        big_square.css('position', 'fixed');
        big_square.css('top', $(this).position().top - window.scrollY + 10); // 10 is for margin
        big_square.css('left', $(this).position().left - window.scrollX + 10);
        big_square.css('width', $(this).width());
        big_square.css('height', $(this).height());
        big_square.css('margin', '0');
        big_square.css('backgroundColor', '#222222');
        big_square.css('z-index', '10');
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
    semwrap.on('click', '.s_s_delete', function() {
        //console.log('delete');
        var s_s_name_div = $(this).closest('.s_s_name_div');
        var semester_name = s_s_name_div.find('.s_s_name').text();

        var semester_square = s_s_name_div.parent();
        var semester_id = semester_square.attr('id');

        if (confirm("Are you sure you want to delete semester \"" + semester_name + "\"?\n" +
        "All data relating to the semester, including classes " +
        "and assignments, will be deleted."))
        {
            $.ajax({
                type:"POST",
                url: "/gradebook/overview/",
                contentType: "application/x-www-form-urlencoded",
                data: {
                    'post_action': 'delete_semester',
                    'delete_semester_id': semester_id.split("_").pop()
                },
                success: function(data) {
                    $('#' + semester_id).remove();
                }
            });
        }
    });
    ////////////////////// renaming semesters //////////////////////
    semwrap.on('click', '.s_s_rename', function() {
        //console.log('rename');
        var s_s_name_div = $(this).closest('.s_s_name_div');
        var semester_name = s_s_name_div.find('.s_s_name').text();

        var new_name = prompt('Enter new Semester Name to replace "' +
            semester_name + '" (ex. "Fall 2014")');

        if (new_name === null || new_name === '') {
            alert('Invalid Semester Name');
            return;
        }

        var semester_square = s_s_name_div.parent();
        var semester_id = semester_square.attr('id');

        $.ajax({
            type:"POST",
            url: "/gradebook/overview/",
            contentType: "application/x-www-form-urlencoded",
            data: {
                'post_action': 'rename_semester',
                'rename_semester_id': semester_id.split("_").pop(),
                'new_semester_name': new_name
            },
            success: function(data) {
                $('#' + semester_id).find('.s_s_name').text(new_name);
            }
        });
    });
    ////////////////////// shrinking large square //////////////////////
    semwrap.on('click', '.large_semester_square', function() {
        //console.log('shrink');
        if (locked)
            return;
        locked = true;
        $(this).animate({
            opacity: '0'
        }, 200, function() {
            $(this).remove();
            locked = false;
        });
        var over = $('#overlay');
        over.animate({
            opacity: '0'
        }, 200, function() {
            over.css('display', 'none');
        });
    });
    ////////////////////// add semesters button color animation //////////////////////
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
    ////////////////////// creating semesters //////////////////////
    add_semester_button.click(function() {
        //console.log('create semester');
        var new_semester_name = prompt('Enter Semester Name (ex. "Fall 2014")');

        if (new_semester_name === null || new_semester_name === '') {
            alert('Invalid Semester Name');
            return;
        }

        $.ajax({
            type:"POST",
            url: "/gradebook/overview/",
            contentType: "application/x-www-form-urlencoded",
            data: {
                'post_action': 'create_semester',
                'new_semester_name': new_semester_name
            },
            success: function(data) {
                $('#add_semester_button').before(
                    "<div class='semester_square' id='semester_" + data.id + "'>" +
                    "    <div class='s_s_name_div'>" +
                    "       <p class='s_s_name'>" + new_semester_name + "</p>" +
                    "       <div class='hidden_in_s_s'>" +
                    "           <p class='mini_link s_s_rename'>rename</p>" +
                    "           <p class='mini_link s_s_delete'>delete</p>" +
                    "       </div>" +
                    "    </div>" +
                    "    <table class='semester_square_course_table'><tbody>" +
                    "        <tr class='hidden_in_s_s add_course_tr'>" +
                    "            <td colspan='3'><p class='mini_link add_course'>add course</p></td>" +
                    "        </tr>" +
                    "    </tbody></table>" +
                    "</div>"
                );
            }
        });
    });
    ////////////////////// adding courses //////////////////////
    semwrap.on('click', '.add_course', function() {
        //console.log('add course');

        var new_course_name = prompt('Enter Class Name (ex. "Intro to Psychology")');

        if (new_course_name === null || new_course_name === '') {
            alert('Invalid Course Name');
            return;
        }

        var s_s_name_div = $(this).closest('.semester_square_course_table');
        var semester_square = s_s_name_div.parent();
        var semester_id = semester_square.attr('id');

        $.ajax({
            type:"POST",
            url: "/gradebook/overview/",
            contentType: "application/x-www-form-urlencoded",
            data: {
                'post_action': 'add_course',
                'new_course_name': new_course_name,
                'semester_id': semester_id.split("_").pop()
            },
            success: function(data) {
                $('#' + semester_id).find('.add_course_tr').before(
                    "<tr>" +
                    "    <td class='s_s_table_data course_number'>XXXXX</td>" +
                    "    <td class='s_s_table_data course_name'>" + new_course_name + "</td>" +
                    "    <td class='s_s_table_data course_grade'>100.0%</td>" +
                    "</tr>"
                );
            }
        });
    });

});
