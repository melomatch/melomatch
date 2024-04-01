$(document).ready(function() {
  $("#scroll").click(function() {
    $("html").animate({ scrollTop: window.innerHeight }, "slow");
  });
});