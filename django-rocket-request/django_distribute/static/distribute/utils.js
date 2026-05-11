/**
 * Renders the list of collected items.
 * @param {object} itemList The list of items to render.
 */
function renderItemList(itemList) {
  $("#item-th").empty();
  $("#count-th").empty();
  $("#itemlist").empty();
  for (var itemName in itemList) {
    $("#itemlist").append(
      "<tr><td scope='row'>" +
        itemName +
        "</td><td>" +
        itemList[itemName] +
        "</td><td><button id='remove-button' data-item-name='" +
        itemName +
        "'>Remove</button></td></tr>",
    );
  }
  $("#user-item-input").val("");
  $("#user-item-input").focus();

  console.log(Object.keys(itemList).length);
  if (Object.keys(itemList).length == 0) {
    $("#item-th").text("No items have been added.");
  } else {
    $("#item-th").text("Item");
    $("#count-th").text("Count");
  }
}
