document.addEventListener("DOMContentLoaded", () => {
    const switchContent = (toShowSelector, toHideSelector, activeButton, inactiveButton) => {
        document.querySelector(toShowSelector).classList.remove("is-hidden");
        document.querySelector(toHideSelector).classList.add("is-hidden");

        document.querySelector(activeButton).classList.add("is-selected-switch-button");
        document.querySelector(inactiveButton).classList.remove("is-selected-switch-button");
    };

    document.querySelector("#top_list_button").on("click", () => {
        switchContent("#top_list_content", "#artist_list_content",
            "#top_list_button", "#artist_list_button");
    });

    document.querySelector("#artist_list_button").on("click", () => {
        switchContent("#artist_list_content", "#top_list_content",
            "#artist_list_button", "#top_list_button");
    });
});