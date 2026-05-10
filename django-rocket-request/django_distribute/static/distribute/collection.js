$(document).ready(function () {
    $("#item-collection-form").on("submit", function (event) {
        event.preventDefault();
        const url = $(this).data("collection-url");
        const csrftoken = Cookies.get("csrftoken")
        $.ajax({
            url: url,
            type: "POST",
            data: {
                "user-item": $("#user-item-input").val(),
                "user-count": $("#user-count-input").val(),
                "csrfmiddlewaretoken": csrftoken
            },
            success: function (response) {
                $("#search-error").empty();
                if (response.itemlist == "Invalid item") {
                    $("#search-error").append("Invalid item");
                    $("#user-item-input").val("");
                    $("#user-item-input").focus();
                }
                if (response.itemlist == "Invalid count") {
                    $("#count-error").append("Invalid count");
                    $("#user-count-input").val("");
                    $("#user-count-input").focus();
                }
                else {
                    $("#item-list").empty();
                    $("#count-list").empty();
                    for (var itemName in response.itemlist) {
                        $("#item-list").append("<li>" + itemName + "</li>");
                        $("#count-list").append("<li>" + response.itemlist[itemName] + "</li>");
                    }
                    $("#user-item-input").val("");
                    $("#user-item-input").focus();
                }
            }
        });
    });
});