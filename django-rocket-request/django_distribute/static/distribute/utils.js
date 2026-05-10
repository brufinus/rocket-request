/**
 * Renders the list of collected items.
 * @param {object} itemList The list of items to render.
 */
function renderItemList(itemList) {
  $("#item-list").empty();
  $("#count-list").empty();
  for (var itemName in itemList) {
    $("#item-list").append("<li>" + itemName + "</li>");
    $("#count-list").append(
      "<li>" +
        itemList[itemName] +
        "<button id='remove-button' data-item-name=\"" +
        itemName +
        '">Remove</button></li>',
    );
  }
  $("#user-item-input").val("");
  $("#user-item-input").focus();
}
