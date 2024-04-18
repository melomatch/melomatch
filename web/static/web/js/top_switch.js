$(document).ready(function () {
    function switchContent(showSelector, hideSelector, activeButton, inactiveButton) {
        let show_block = $(showSelector);
        let hide_block = $(hideSelector);
        show_block.removeClass('is-hidden');
        hide_block.addClass('is-hidden');
        $(activeButton).addClass('is-selected-switch-button');
        $(inactiveButton).removeClass('is-selected-switch-button');
    }

    $("#top_list_button").on("click", function () {
        switchContent('#top_list_content', '#artist_list_content',
            '#top_list_button', '#artist_list_button');
    });

    $("#artist_list_button").on("click", function () {
        switchContent('#artist_list_content', '#top_list_content',
            '#artist_list_button', '#top_list_button');
    });
});