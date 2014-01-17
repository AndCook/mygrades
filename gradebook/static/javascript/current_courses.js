$(document).ready(function () {
    var squares = $('.semester_square');
    squares.addClass('large_semester_square');
    squares.removeClass('semester_square');

    squares.find('.hidden_in_s_s_inline').css('display', 'inline-block');
    squares.find('.hidden_in_s_s_block').css('display', 'block');
    squares.find('.hidden_in_s_s_table_row').css('display', 'table-row');
    squares.find('.hidden_in_s_s_table_cell').css('display', 'table-cell');
    resize_course_table_columns();
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