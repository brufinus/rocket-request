/**
 * Handles item removal on click using AJAX.
 */
$(document).ready(function () {
  const url = $("article").data("remove-url");
  const csrftoken = Cookies.get("csrftoken");
  $(document).on("click", "#remove-button", function () {
    const itemName = $(this).data("item-name");
    $.ajax({
      url: url,
      type: "POST",
      data: {
        "user-item": itemName,
        csrfmiddlewaretoken: csrftoken,
      },
      success: function (response) {
        $("#search-error").empty();
        renderItemList(response.itemlist);
      },
    });
  });
});
