$(document).ready(function() {
    let path_name = window.location.pathname;
    $("#top_list_button").on("click", function () {
        let show_block = document.querySelector('#top_list_content');
        let hide_block = document.querySelector('#artist_list_content');
        show_block.classList.remove('is-hidden')
        hide_block.classList.add('is-hidden')
        $(this).addClass('is-selected-switch-button')
        $("#artist_list_button").removeClass('is-selected-switch-button')
    });
    $("#artist_list_button").on("click", function () {
        let show_block = document.querySelector('#artist_list_content');
        let hide_block = document.querySelector('#top_list_content');
        show_block.classList.remove('is-hidden')
        hide_block.classList.add('is-hidden')
        $(this).addClass('is-selected-switch-button')
        $("#top_list_button").removeClass('is-selected-switch-button')

    });
})
