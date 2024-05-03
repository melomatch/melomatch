document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".notification .delete").forEach((closeButton) => {
    closeButton.addEventListener("click", () => {
      closeButton.closest(".notification").remove();
    });
  });
});