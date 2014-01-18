$(document).ready(function() {
    var semwrap = $('#semester_squares_wrapper');
    var locked = false;
    ////////////////////// expanding a square //////////////////////
    semwrap.on('click', '.semester_square', function() {
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

        var new_width = Math.max(.65*$(window).innerWidth(), 600);
        var new_height = Math.max(.65*$(window).innerHeight(), 450);

        $(this).after(big_square);

        big_square.animate({
            width: new_width,
            height: new_height,
            left: ($(window).innerWidth() - new_width) / 2,
            top: ($(window).innerHeight() - new_height) / 2
        }, 200, function() {
            big_square.css('min-width', '600px');
            big_square.css('min-height', '450px');
            locked = false;
        });
        var over = $('#overlay');
        over.css('height', $('#middle_section').height());
        over.css('display', 'block');
        over.animate({
            opacity: '0.3'
        }, 200);

        big_square.css('font-size', '1.3em');
        big_square.find('.hidden_in_s_s_inline').css('display', 'inline-block');
        big_square.find('.hidden_in_s_s_block').css('display', 'block');
        big_square.find('.hidden_in_s_s_table_row').css('display', 'table-row');
        big_square.find('.hidden_in_s_s_table_cell').css('display', 'table-cell');
        resize_course_table_columns();

        $(window).resize(function () {
            big_square.css('left', ($(window).innerWidth() - big_square.width()) / 2);
            big_square.css('top', ($(window).innerHeight() - big_square.height()) / 2);
        });
    });
    function resize_course_table_columns() {
        var big_square = $('.large_semester_square');
        big_square.find('.course_number').css('width', '13%');
        big_square.find('.course_hours').css('width', '8%');
        big_square.find('.course_name').css('width', '35%');
        big_square.find('.course_instructor').css('width', '25%');
        big_square.find('.course_grade').css('width', '10%');
        big_square.find('.course_edit').css('width', '4%');
        big_square.find('.course_delete').css('width', '5%');
    }
    ////////////////////// shrinking large square //////////////////////
    $('#overlay, #header, #footer').click( function() {
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
    ////////////////////// disable coure_link's in semester_square //////////////////////
    semwrap.on('click', '.semester_square .course_link', function(e) {
        e.preventDefault();
    });
});
