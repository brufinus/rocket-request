/**
 * Adds a class to apply CSS to the nav item for the current context.
 */
$(document).ready(function () {
  $("a.nav-bar-item").each(function () {
    if ($(this).prop("href") == window.location.href) {
      $(this).addClass("nav-bar-item-context");
    }
  });
});
