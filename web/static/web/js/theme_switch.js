$(document).ready(function(){
    var savedTheme = localStorage.getItem("bulma-theme");
    if (savedTheme) {
        $("html").attr("data-theme", savedTheme);
        updateThemeIcon(savedTheme);
    }

    $("#theme-icon").click(function(){
        var currentTheme = $("html").attr("data-theme");
        var newTheme = currentTheme === "dark" ? "light" : "dark";
        $("html").attr("data-theme", newTheme);
        localStorage.setItem("bulma-theme", newTheme);
        updateThemeIcon(newTheme);
    });

    function updateThemeIcon(theme) {
        var iconClass = theme === "dark" ? "fa-moon" : "fa-sun";
        $("#theme-icon").removeClass("fa-moon fa-sun").addClass(iconClass);
    }
});