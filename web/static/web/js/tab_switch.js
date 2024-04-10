$(document).ready(function() {
    let path_name = window.location.pathname;
    $("#tabs").children().each(function() {
        if (path_name.includes(this.id)) {
            $(this).addClass('is-active');
        }
    });
});