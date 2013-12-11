$(function() {
    // on hover over all semester-square's, change the background-color to #3b3b3b from #222222
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
    semwrap.on('mouseenter', '.large_semester_square', function() {
        $(this).animate({
            backgroundColor: '#3b3b3b'
        }, 100);
    });
    semwrap.on('mouseleave', '.large_semester_square', function() {
        $(this).animate({
            backgroundColor: '#222222'
        }, 100);
    });

    var locked = false;

    semwrap.on('click', '.semester_square', function() {
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
        big_square.css('backgroundColor', '#3b3b3b');
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

    });
    semwrap.on('click', '.large_semester_square', function() {
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

