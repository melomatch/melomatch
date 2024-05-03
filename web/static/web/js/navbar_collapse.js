document.addEventListener("DOMContentLoaded", () => {
  document.querySelector("#navbarBurger").on("click", () => {
    document.querySelector("#navbarBurger").classList.toggle("is-active");
    document.querySelector("#navbarMenu").classList.toggle("is-active");
  });
});