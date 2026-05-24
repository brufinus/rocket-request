/**
 * On enter, submits the form of which the textarea belongs to.
 */
$(document).ready(function () {
  $("#blueprint-input").keypress(function (event) {
    if (event.key == "Enter") {
      event.preventDefault();
      $(this).closest("form").submit();
    }
  });
});
