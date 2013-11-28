$(function() {
    // on hover over all semester-square's, change the background-color to #3b3b3b from #222222
    var semester_squares = $('.semester_square');
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
    /*semester_squares.click(function() {
        $(this).css('z-index', '1000');
        $(this).css('position', 'absolute');
        $(this).animate({
            width: '98%',
            height: '900px'
        }, 250);
    });*/

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
});
