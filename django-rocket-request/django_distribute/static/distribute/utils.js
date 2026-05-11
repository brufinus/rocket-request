/**
 * Renders the list of collected items.
 * @param {object} itemList The list of items to render.
 */
function renderItemList(itemList) {
  $("#itemlist").empty();
  $("#count-list").empty();
  for (var itemName in itemList) {
    $("#itemlist").append(
      "<tr><td scope='row'>" +
        itemName +
        "</td><td>" +
        itemList[itemName] +
        "</td><td><button id='remove-button' data-item-name=" +
        itemName +
        ">Remove</button></td></tr>",
    );
  }
  $("#user-item-input").val("");
  $("#user-item-input").focus();
}
