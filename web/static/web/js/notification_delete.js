$(document).ready(function() {
  $('.notification .delete').on('click', function() {
    $(this).parent('.notification').remove();
  });
});