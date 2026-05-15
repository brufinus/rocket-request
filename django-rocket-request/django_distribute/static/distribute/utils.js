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
      "<tr>" +
        '<td class="remove-data"><button id="remove-button" style="font-size:24px" data-item-name="' +
        itemName +
        '"><i class="fa fa-trash-o"></i></button></td>' +
        "<td class='added-item' scope='row'>" +
        itemName +
        "</td><td>" +
        itemList[itemName] +
        "</td></tr>",
    );
  }
  $("#user-item-input").val("");
  $("#user-item-input").focus();

  if (Object.keys(itemList).length == 0) {
    $("#item-th").text("No items have been added.");
  } else {
    $("#item-th").text("Item");
    $("#count-th").text("Count");
  }
}
