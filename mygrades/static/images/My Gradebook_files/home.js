$(function() {
    var sort = $("#sortable-courselist");
    sort.sortable({
      	placeholder: "course placeholder"
    });
    sort.disableSelection();
});

$(function() {
    var sort2 = $(".sortable-assignmentlist");
    sort2.sortable({
      	placeholder: "assignment placeholder"
    });
    sort2.disableSelection();
});
