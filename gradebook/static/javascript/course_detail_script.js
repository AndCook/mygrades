$(document).ready(function() {
    var report_final_grade_dialog = $('#report_final_grade_dialog_box');
    var final_grade_dropdown = $('#final_grade_dropdown');
    var grades = ['#', 'A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+',
        'C', 'C-', 'D+', 'D', 'D-', 'F', 'CR', 'NC', 'P', 'FL', 'W'];
    final_grade_dropdown.jqxDropDownList({ source: grades, selectedIndex: 0, width: '50', height: '25'});
    var report_final_grade_button = $('#report_final_grade');
    report_final_grade_button.button().click(function() {
        report_final_grade_dialog.dialog('open');
    });
    report_final_grade_dialog.dialog({
		autoOpen: false,
		width: 350,
        resizable: false,
		modal: true,
		buttons: {
			'Report Grade': {
                text: 'Save Grade',
                click: function() {

                    var course_id = $('.course_name').attr('id').split('_').pop();
                    var final_grade = final_grade_dropdown.val();
                    console.log(final_grade);

                    $.ajax({
                        type:"POST",
                        url: "/gradebook/course_detail/" + course_id + "/",
                        contentType: "application/x-www-form-urlencoded",
                        data: {
                            'post_action': 'report_final_grade',
                            'final_grade': final_grade
                        },
                        success: function() {
                            report_final_grade_dialog.dialog('close');
                            $('#final_grade').text(final_grade);
                            var report_final_grade_button = $('#report_final_grade').find('.ui-button-text');
                            if (final_grade === '#')
                                report_final_grade_button.text('Report Final Grade');
                            else
                                report_final_grade_button.text('Change Final Grade');
                        }
                    });
                }
	      	},
		  	Cancel: function() {
	  			report_final_grade_dialog.dialog('close');
		  	}
        },
        close: function() {
        }
	});
});