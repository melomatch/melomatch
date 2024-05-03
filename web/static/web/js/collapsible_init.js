document.addEventListener("DOMContentLoaded", () => {
  // according to https://github.com/CreativeBulma/bulma-collapsible/issues/15#issuecomment-1686574119
  const bulmaCollapsibleInstances = bulmaCollapsible.attach(".is-collapsible");

  bulmaCollapsibleInstances.forEach((collapsibleElement) => {
    collapsibleElement.on("after:collapse", (item) => {
      item.element.parentNode.querySelector(".rotate").classList.add("down");
    });

    collapsibleElement.on("before:expand", (item) => {
      item.element.parentNode.querySelector(".rotate").classList.remove("down");
    });

    // according to https://github.com/CreativeBulma/bulma-collapsible/issues/13#issuecomment-1434178874
    collapsibleElement.on("after:expand", (item) => {
      item._originalHeight = item.element.scrollHeight + "px";
    });
  });
});