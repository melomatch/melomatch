document.addEventListener("DOMContentLoaded", () => {
    const htmlTag = document.querySelector("html");
    const themeIconTag = document.querySelector("#theme-icon");
    const savedTheme = localStorage.getItem("bulma-theme");
    const updateThemeIcon = (theme) => {
        const iconClass = theme === "dark" ? "fa-moon" : "fa-sun";
        themeIconTag.classList.remove("fa-moon", "fa-sun");
        themeIconTag.classList.add(iconClass);
    };

    if (savedTheme) {
        htmlTag.setAttribute("data-theme", savedTheme);
        updateThemeIcon(savedTheme);
    }

    document.querySelector("#theme-icon").on("click", () => {
        const currentTheme = htmlTag.getAttribute("data-theme");
        const newTheme = currentTheme === "dark" ? "light" : "dark";
        htmlTag.setAttribute("data-theme", newTheme);
        localStorage.setItem("bulma-theme", newTheme);
        updateThemeIcon(newTheme);
    });
});