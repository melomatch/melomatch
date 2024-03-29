$(document).ready(function() {
  const bulmaCollapsibleInstances = bulmaCollapsible.attach(".is-collapsible");

  bulmaCollapsibleInstances.forEach(function (collapsibleElement) {
    collapsibleElement.on("after:collapse", (item) => {
      console.log(item.element.parentNode.querySelector(".rotate"))
      item.element.parentNode.querySelector(".rotate").classList.add("down");
    })

    collapsibleElement.on("before:expand", (item) => {
      item.element.parentNode.querySelector(".rotate").classList.remove("down");
    })

    collapsibleElement.on("after:expand", (item) => {
      item._originalHeight = item.element.scrollHeight + "px";
    })
  })
});