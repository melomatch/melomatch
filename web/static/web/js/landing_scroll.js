document.addEventListener("DOMContentLoaded", () => {
  document.querySelector("#scroll").on("click", () => {
    window.scroll({
      top: window.innerHeight,
      behavior: "smooth",
    });
  });
});